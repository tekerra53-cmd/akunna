import { Router, type Request, type Response } from "express";
import { db } from "@workspace/db";
import { diseasesTable } from "@workspace/db";
import { eq } from "drizzle-orm";
import { GetDiseaseImagesParams } from "@workspace/api-zod";

const router = Router();

const DISEASE_SEARCH_TERMS: Record<string, { inat: string; wiki: string; wikiLab: string }> = {
  "Cassava Mosaic Virus": {
    inat: "cassava mosaic yellow leaf",
    wiki: "cassava mosaic disease leaf symptom",
    wikiLab: "cassava mosaic virus plant pathology",
  },
  "Cassava Bacterial Blight": {
    inat: "cassava disease blight leaf",
    wiki: "cassava bacterial blight leaf necrosis",
    wikiLab: "Xanthomonas plant bacterial blight pathogen",
  },
  "Maize Northern Leaf Blight": {
    inat: "corn leaf blight disease",
    wiki: "maize northern leaf blight fungal disease",
    wikiLab: "Helminthosporium turcicum fungal pathogen",
  },
  "Maize Common Rust": {
    inat: "corn rust fungal disease",
    wiki: "maize common rust Puccinia orange pustule",
    wikiLab: "Puccinia rust urediniospores microscope",
  },
  "Tomato Late Blight": {
    inat: "tomato late blight Phytophthora",
    wiki: "tomato late blight disease necrosis",
    wikiLab: "Phytophthora infestans sporangium fungal",
  },
  "Tomato Leaf Mold": {
    inat: "tomato leaf mold fungal",
    wiki: "tomato leaf mold Cladosporium olive mold",
    wikiLab: "Cladosporium fulvum conidiophore microscopy",
  },
  "Rice Leaf Blast": {
    inat: "rice blast disease",
    wiki: "rice blast Magnaporthe disease lesion",
    wikiLab: "Magnaporthe oryzae conidia pathogen",
  },
  "Potato Early Blight": {
    inat: "potato early blight Alternaria",
    wiki: "potato early blight target spot Alternaria",
    wikiLab: "Alternaria solani fungal conidia microscope",
  },
  "Healthy": {
    inat: "healthy green cassava leaf",
    wiki: "healthy crop plant green leaf farm",
    wikiLab: "plant leaf stomata cell anatomy microscope",
  },
};

interface INatPhoto {
  url: string;
  license_code?: string;
  attribution?: string;
}

interface INatObservation {
  photos?: INatPhoto[];
  taxon?: { name?: string };
  user?: { login?: string };
}

interface WikiPage {
  pageid: number;
  imageinfo?: Array<{ url: string; extmetadata?: { Artist?: { value: string }; LicenseShortName?: { value: string } } }>;
}

async function fetchInatFieldImages(query: string): Promise<Array<{ url: string; attribution: string; source: string; licenseCode: string | null }>> {
  const tryFetch = async (q: string): Promise<Array<{ url: string; attribution: string; source: string; licenseCode: string | null }>> => {
    const encoded = encodeURIComponent(q);
    const url = `https://api.inaturalist.org/v1/observations?q=${encoded}&photos=true&per_page=6&license=cc-by,cc-by-sa,cc0,cc-by-nc`;
    const res = await fetch(url, { signal: AbortSignal.timeout(8000) });
    if (!res.ok) return [];
    const data = (await res.json()) as { results?: INatObservation[] };
    const results: Array<{ url: string; attribution: string; source: string; licenseCode: string | null }> = [];

    for (const obs of data.results ?? []) {
      for (const photo of obs.photos ?? []) {
        if (photo.url) {
          const highRes = photo.url.replace("/square.", "/large.").replace("/thumb.", "/large.");
          results.push({
            url: highRes,
            attribution: photo.attribution ?? `© ${obs.user?.login ?? "iNaturalist user"} (iNaturalist)`,
            source: "iNaturalist",
            licenseCode: photo.license_code ?? null,
          });
        }
      }
      if (results.length >= 4) break;
    }

    return results;
  };

  try {
    const primary = await tryFetch(query);
    if (primary.length > 0) return primary;

    // Fallback: strip to first two words for broader search
    const shortQuery = query.split(" ").slice(0, 2).join(" ");
    if (shortQuery !== query) {
      return await tryFetch(shortQuery);
    }
    return [];
  } catch {
    return [];
  }
}

async function fetchWikimediaLabImages(query: string): Promise<Array<{ url: string; attribution: string; source: string; licenseCode: string | null }>> {
  try {
    const encoded = encodeURIComponent(query);
    const searchUrl = `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=${encoded}&srnamespace=6&format=json&srlimit=6&origin=*`;
    const searchRes = await fetch(searchUrl, { signal: AbortSignal.timeout(8000) });
    if (!searchRes.ok) return [];
    const searchData = (await searchRes.json()) as { query?: { search?: Array<{ pageid: number }> } };
    const pageIds = (searchData.query?.search ?? [])
      .slice(0, 4)
      .map((r) => r.pageid)
      .join("|");

    if (!pageIds) return [];

    const infoUrl = `https://commons.wikimedia.org/w/api.php?action=query&pageids=${pageIds}&prop=imageinfo&iiprop=url|extmetadata&format=json&iiurlwidth=800&origin=*`;
    const infoRes = await fetch(infoUrl, { signal: AbortSignal.timeout(8000) });
    if (!infoRes.ok) return [];
    const infoData = (await infoRes.json()) as { query?: { pages?: Record<string, WikiPage> } };

    const results: Array<{ url: string; attribution: string; source: string; licenseCode: string | null }> = [];

    for (const page of Object.values(infoData.query?.pages ?? {})) {
      const info = page.imageinfo?.[0];
      if (info?.url && /\.(jpg|jpeg|png|gif|svg)$/i.test(info.url)) {
        const artist = info.extmetadata?.Artist?.value?.replace(/<[^>]+>/g, "") ?? "Wikimedia contributor";
        const license = info.extmetadata?.LicenseShortName?.value ?? null;
        results.push({
          url: info.url,
          attribution: `© ${artist}`,
          source: "Wikimedia Commons",
          licenseCode: license,
        });
      }
    }

    return results;
  } catch {
    return [];
  }
}

router.get("/diseases/:id/images", async (req: Request, res: Response) => {
  const parsed = GetDiseaseImagesParams.safeParse(req.params);
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

  const terms = DISEASE_SEARCH_TERMS[disease.name] ?? {
    inat: disease.name.toLowerCase(),
    wiki: disease.name.toLowerCase(),
    wikiLab: disease.name.toLowerCase(),
  };

  const [fieldImages, labImages] = await Promise.all([
    fetchInatFieldImages(terms.inat),
    fetchWikimediaLabImages(terms.wikiLab),
  ]);

  res.json({ fieldImages, labImages });
});

export default router;
