import { Router, type Request, type Response } from "express";
import { db } from "@workspace/db";
import { diseasesTable } from "@workspace/db";
import { eq } from "drizzle-orm";
import { GetDiseaseParams } from "@workspace/api-zod";

const router = Router();

router.get("/diseases", async (_req: Request, res: Response) => {
  const diseases = await db.select().from(diseasesTable);
  res.json(diseases);
});

router.get("/diseases/:id", async (req: Request, res: Response) => {
  const parsed = GetDiseaseParams.safeParse(req.params);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid id" });
    return;
  }

  const [disease] = await db
    .select()
    .from(diseasesTable)
    .where(eq(diseasesTable.id, parsed.data.id));

  if (!disease) {
    res.status(404).json({ error: "Disease not found" });
    return;
  }

  res.json(disease);
});

export default router;
