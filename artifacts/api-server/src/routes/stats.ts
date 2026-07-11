import { Router, type Request, type Response } from "express";
import { db } from "@workspace/db";
import { predictionsTable } from "@workspace/db";
import { desc, sql, count, avg } from "drizzle-orm";

const router = Router();

router.get("/stats/summary", async (_req: Request, res: Response) => {
  const totalResult = await db
    .select({ total: count() })
    .from(predictionsTable);

  const healthyResult = await db
    .select({ healthy: count() })
    .from(predictionsTable)
    .where(sql`${predictionsTable.isHealthy} = true`);

  const avgResult = await db
    .select({ avg: avg(predictionsTable.confidence) })
    .from(predictionsTable);

  const mostCommonResult = await db
    .select({
      name: predictionsTable.diseaseName,
      cnt: count(),
    })
    .from(predictionsTable)
    .where(sql`${predictionsTable.isHealthy} = false`)
    .groupBy(predictionsTable.diseaseName)
    .orderBy(sql`count(*) desc`)
    .limit(1);

  const totalScans = Number(totalResult[0]?.total ?? 0);
  const healthyPlants = Number(healthyResult[0]?.healthy ?? 0);
  const diseasesDetected = totalScans - healthyPlants;
  const averageConfidence = Number(avgResult[0]?.avg ?? 0);
  const mostCommonDisease = mostCommonResult[0]?.name ?? null;

  res.json({
    totalScans,
    diseasesDetected,
    healthyPlants,
    averageConfidence,
    mostCommonDisease,
  });
});

router.get("/stats/disease-distribution", async (_req: Request, res: Response) => {
  const totalResult = await db
    .select({ total: count() })
    .from(predictionsTable);
  const total = Number(totalResult[0]?.total ?? 1);

  const distribution = await db
    .select({
      diseaseName: predictionsTable.diseaseName,
      cnt: count(),
    })
    .from(predictionsTable)
    .groupBy(predictionsTable.diseaseName)
    .orderBy(sql`count(*) desc`);

  const result = distribution.map(row => ({
    diseaseName: row.diseaseName,
    count: Number(row.cnt),
    percentage: (Number(row.cnt) / total) * 100,
  }));

  res.json(result);
});

router.get("/stats/recent-activity", async (_req: Request, res: Response) => {
  const recent = await db
    .select()
    .from(predictionsTable)
    .orderBy(desc(predictionsTable.createdAt))
    .limit(10);
  res.json(recent);
});

export default router;
