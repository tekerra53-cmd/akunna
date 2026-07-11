import { Router, type Request, type Response } from "express";
import { db } from "@workspace/db";
import { predictionsTable } from "@workspace/db";
import { eq, desc, count, avg, sql } from "drizzle-orm";
import { CreatePredictionBody, GetPredictionParams } from "@workspace/api-zod";

const router = Router();

const DISEASE_DB = [
  { name: "Healthy", isHealthy: true, severity: "low" as const, treatment: "No action needed. Plant is healthy.", cropType: "any" },
  { name: "Cassava Mosaic Virus", isHealthy: false, severity: "high" as const, treatment: "Remove and destroy infected plants immediately. Use certified disease-free cassava cuttings. Control whitefly vectors with insecticides.", cropType: "cassava" },
  { name: "Cassava Bacterial Blight", isHealthy: false, severity: "medium" as const, treatment: "Remove infected leaves and stems. Apply copper-based bactericide. Use resistant varieties.", cropType: "cassava" },
  { name: "Maize Northern Leaf Blight", isHealthy: false, severity: "medium" as const, treatment: "Apply fungicides containing strobilurin or triazole. Plant resistant hybrids. Practice crop rotation.", cropType: "maize" },
  { name: "Maize Common Rust", isHealthy: false, severity: "low" as const, treatment: "Apply sulfur-based fungicide. Use resistant maize varieties. Monitor and spray early in the season.", cropType: "maize" },
  { name: "Tomato Late Blight", isHealthy: false, severity: "high" as const, treatment: "Apply copper fungicide immediately. Remove infected tissue. Avoid overhead irrigation. Use resistant varieties.", cropType: "tomato" },
  { name: "Tomato Leaf Mold", isHealthy: false, severity: "medium" as const, treatment: "Improve air circulation. Apply chlorothalonil or mancozeb fungicide. Reduce humidity in greenhouse.", cropType: "tomato" },
  { name: "Rice Leaf Blast", isHealthy: false, severity: "high" as const, treatment: "Apply tricyclazole or isoprothiolane fungicide. Avoid excessive nitrogen. Use resistant varieties.", cropType: "rice" },
  { name: "Potato Early Blight", isHealthy: false, severity: "medium" as const, treatment: "Apply chlorothalonil fungicide every 7-10 days. Maintain proper plant nutrition. Remove infected leaves.", cropType: "potato" },
];

function simulatePrediction(cropType: string) {
  const cropDiseases = DISEASE_DB.filter(d => d.cropType === cropType || d.cropType === "any");
  const pool = cropDiseases.length > 0 ? cropDiseases : DISEASE_DB;
  
  const rand = Math.random();
  let selected;
  if (rand < 0.35) {
    selected = DISEASE_DB.find(d => d.isHealthy) || pool[0];
  } else {
    const diseases = pool.filter(d => !d.isHealthy);
    selected = diseases[Math.floor(Math.random() * diseases.length)] || pool[0];
  }

  const confidence = selected.isHealthy
    ? 0.75 + Math.random() * 0.24
    : 0.60 + Math.random() * 0.35;

  return {
    diseaseName: selected.name,
    isHealthy: selected.isHealthy,
    severity: selected.severity,
    treatment: selected.treatment,
    confidence: Math.min(confidence, 0.99),
  };
}

router.get("/predictions", async (req: Request, res: Response) => {
  const predictions = await db
    .select()
    .from(predictionsTable)
    .orderBy(desc(predictionsTable.createdAt));
  res.json(predictions);
});

router.post("/predictions", async (req: Request, res: Response) => {
  const parsed = CreatePredictionBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid request body" });
    return;
  }

  const { cropType } = parsed.data;
  const result = simulatePrediction(cropType);

  const [prediction] = await db
    .insert(predictionsTable)
    .values({
      cropType,
      diseaseName: result.diseaseName,
      confidence: result.confidence,
      severity: result.severity,
      treatment: result.treatment,
      isHealthy: result.isHealthy,
      imageUrl: parsed.data.imageUrl ?? null,
    })
    .returning();

  res.status(201).json(prediction);
});

router.get("/predictions/:id", async (req: Request, res: Response) => {
  const parsed = GetPredictionParams.safeParse(req.params);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid id" });
    return;
  }

  const [prediction] = await db
    .select()
    .from(predictionsTable)
    .where(eq(predictionsTable.id, parsed.data.id));

  if (!prediction) {
    res.status(404).json({ error: "Prediction not found" });
    return;
  }

  res.json(prediction);
});

export default router;
