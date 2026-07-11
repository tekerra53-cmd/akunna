from .models import Disease

DISEASE_LIBRARY = [
    # Cassava diseases
    {
        "name": "Cassava Bacterial Blight",
        "crop_type": "cassava",
        "description": "A bacterial disease that causes wilting, dieback, and significant cassava yield loss.",
        "symptoms": "Angular water-soaked leaf spots, blight, stem cankers, and leaf drop.",
        "treatment": "Use clean cuttings, remove infected plants, and apply copper-based bactericides where appropriate.",
        "severity": "high",
    },
    {
        "name": "Cassava Brown Streak Disease",
        "crop_type": "cassava",
        "description": "A viral disease that damages roots and leads to severe quality and yield reduction.",
        "symptoms": "Yellow chlorosis patterns on leaves and brown necrosis in storage roots.",
        "treatment": "Plant resistant varieties, rogue infected plants early, and control whitefly vectors.",
        "severity": "high",
    },
    {
        "name": "Cassava Green Mottle",
        "crop_type": "cassava",
        "description": "Viral infection causing mosaic/mottle discoloration and stunted growth.",
        "symptoms": "Mottled green-yellow leaves, wrinkling, and reduced vigor.",
        "treatment": "Use certified planting material and maintain vector control through integrated pest management.",
        "severity": "medium",
    },
    {
        "name": "Cassava Mosaic Disease",
        "crop_type": "cassava",
        "description": "A widespread cassava viral disease affecting photosynthesis and root development.",
        "symptoms": "Distinct mosaic/chlorotic leaf patches, deformation, and stunting.",
        "treatment": "Use resistant varieties, remove diseased plants, and manage whiteflies.",
        "severity": "high",
    },
    
    # Maize/Corn diseases
    {
        "name": "Maize Common Rust",
        "crop_type": "maize",
        "description": "Fungal disease often appearing in humid environments.",
        "symptoms": "Small cinnamon-brown pustules on both leaf surfaces.",
        "treatment": "Use resistant hybrids and apply recommended fungicides when disease pressure is high.",
        "severity": "medium",
    },
    {
        "name": "Maize Northern Leaf Blight",
        "crop_type": "maize",
        "description": "A major maize fungal disease causing elongated lesions and reduced photosynthetic area.",
        "symptoms": "Long cigar-shaped gray-green lesions that turn tan.",
        "treatment": "Rotate crops, plant resistant hybrids, and apply fungicides at early onset.",
        "severity": "high",
    },
    {
        "name": "Maize Gray Leaf Spot",
        "crop_type": "maize",
        "description": "Fungal disease affecting grain fill and yield in warm humid climates.",
        "symptoms": "Rectangular leaf lesions between veins, often gray to brown.",
        "treatment": "Crop residue management, resistant varieties, and timely fungicide applications.",
        "severity": "high",
    },
    {
        "name": "Maize Southern Leaf Blight",
        "crop_type": "maize",
        "description": "Fungal disease causing significant yield losses in susceptible hybrids.",
        "symptoms": "Large tan lesions with parallel edges, often covering entire leaves.",
        "treatment": "Plant resistant hybrids, practice crop rotation, and apply fungicides when conditions favor disease.",
        "severity": "high",
    },
    {
        "name": "Maize Tar Spot",
        "crop_type": "maize",
        "description": "Emerging fungal disease causing small black raised structures on leaves.",
        "symptoms": "Small black tar-like spots on leaves, sometimes with yellow halos.",
        "treatment": "Use resistant hybrids, apply fungicides preventively, and manage crop residue.",
        "severity": "high",
    },
    
    # Tomato diseases
    {
        "name": "Tomato Early Blight",
        "crop_type": "tomato",
        "description": "Fungal disease that progresses from older leaves upward.",
        "symptoms": "Concentric ring lesions with yellowing around spots.",
        "treatment": "Remove infected leaves, avoid overhead irrigation, and apply preventive fungicide.",
        "severity": "medium",
    },
    {
        "name": "Tomato Late Blight",
        "crop_type": "tomato",
        "description": "Aggressive disease that can rapidly destroy tomato crops under moist conditions.",
        "symptoms": "Water-soaked lesions, dark blight patches, and white mold under leaves.",
        "treatment": "Immediate sanitation, weather-based fungicide scheduling, and resistant varieties.",
        "severity": "high",
    },
    {
        "name": "Tomato Leaf Mold",
        "crop_type": "tomato",
        "description": "Common in high humidity greenhouses and dense canopies.",
        "symptoms": "Yellow spots on upper leaves with olive-green mold below.",
        "treatment": "Improve airflow, reduce humidity, and apply protective fungicides.",
        "severity": "medium",
    },
    {
        "name": "Tomato Septoria Leaf Spot",
        "crop_type": "tomato",
        "description": "Fungal disease causing extensive defoliation if left untreated.",
        "symptoms": "Small circular spots with gray centers and dark borders on lower leaves.",
        "treatment": "Remove infected foliage, mulch to prevent soil splash, and apply fungicides regularly.",
        "severity": "medium",
    },
    {
        "name": "Tomato Bacterial Spot",
        "crop_type": "tomato",
        "description": "Bacterial disease affecting leaves and fruit quality.",
        "symptoms": "Small dark spots with yellow halos on leaves, raised spots on fruit.",
        "treatment": "Use disease-free transplants, copper sprays, and avoid overhead watering.",
        "severity": "medium",
    },
    {
        "name": "Tomato Fusarium Wilt",
        "crop_type": "tomato",
        "description": "Soil-borne fungal disease causing vascular wilting.",
        "symptoms": "Yellowing and wilting of lower leaves, brown vascular tissue in stems.",
        "treatment": "Use resistant varieties, practice crop rotation, and solarize soil before planting.",
        "severity": "high",
    },
    {
        "name": "Tomato Verticillium Wilt",
        "crop_type": "tomato",
        "description": "Fungal disease causing progressive wilting and yield loss.",
        "symptoms": "V-shaped yellow lesions on leaf margins, wilting during day.",
        "treatment": "Plant resistant varieties, rotate with non-host crops, and maintain soil health.",
        "severity": "high",
    },
    {
        "name": "Tomato Mosaic Virus",
        "crop_type": "tomato",
        "description": "Viral disease causing mottled leaves and reduced fruit quality.",
        "symptoms": "Mottled light and dark green patterns on leaves, distorted growth.",
        "treatment": "Use virus-free seed, sanitize tools, remove infected plants, and control aphid vectors.",
        "severity": "medium",
    },
    
    # Potato diseases
    {
        "name": "Potato Early Blight",
        "crop_type": "potato",
        "description": "Fungal disease causing progressive leaf defoliation.",
        "symptoms": "Dark spots with concentric rings, usually on older leaves first.",
        "treatment": "Rotate crops, improve nutrition, and use fungicides preventively.",
        "severity": "medium",
    },
    {
        "name": "Potato Late Blight",
        "crop_type": "potato",
        "description": "Highly destructive oomycete disease under cool, wet conditions.",
        "symptoms": "Dark leaf lesions, white sporulation, and stem collapse.",
        "treatment": "Destroy volunteer plants, monitor weather alerts, and use targeted fungicide programs.",
        "severity": "high",
    },
    {
        "name": "Potato Blackleg",
        "crop_type": "potato",
        "description": "Bacterial disease causing stem rot and tuber decay.",
        "symptoms": "Black rotting at stem base, yellowing leaves, and soft rot in tubers.",
        "treatment": "Use certified seed potatoes, improve drainage, and remove infected plants promptly.",
        "severity": "high",
    },
    {
        "name": "Potato Common Scab",
        "crop_type": "potato",
        "description": "Bacterial disease affecting tuber skin quality.",
        "symptoms": "Rough corky lesions on tuber surface, reduced marketability.",
        "treatment": "Maintain soil pH below 5.5, use resistant varieties, and ensure adequate soil moisture.",
        "severity": "low",
    },
    
    # Rice diseases
    {
        "name": "Rice Bacterial Blight",
        "crop_type": "rice",
        "description": "A bacterial disease that spreads quickly in warm, wet fields.",
        "symptoms": "Yellowing leaf tips that expand into straw-colored streaks.",
        "treatment": "Use tolerant varieties, balanced fertilization, and reduce standing water stress where possible.",
        "severity": "high",
    },
    {
        "name": "Rice Blast",
        "crop_type": "rice",
        "description": "A major fungal disease impacting leaves and panicles.",
        "symptoms": "Diamond-shaped lesions with gray centers and brown margins.",
        "treatment": "Use resistant varieties, avoid excess nitrogen, and apply fungicides early.",
        "severity": "high",
    },
    {
        "name": "Rice Brown Spot",
        "crop_type": "rice",
        "description": "Fungal disease often linked with nutrient stress and poor field conditions.",
        "symptoms": "Small brown circular to oval lesions that enlarge over time.",
        "treatment": "Improve field nutrition, use clean seed, and apply fungicide when needed.",
        "severity": "medium",
    },
    {
        "name": "Rice Tungro",
        "crop_type": "rice",
        "description": "Viral disease spread by leafhoppers causing severe stunting.",
        "symptoms": "Yellow-orange discoloration, reduced tillering, and stunted plants.",
        "treatment": "Control vectors, use resistant varieties, and remove infected plants quickly.",
        "severity": "high",
    },
    {
        "name": "Rice Sheath Blight",
        "crop_type": "rice",
        "description": "Fungal disease affecting stems and sheaths in humid conditions.",
        "symptoms": "Oval to irregular lesions on leaf sheaths, greenish-gray with brown borders.",
        "treatment": "Manage plant density, apply fungicides at early infection, and use balanced fertilization.",
        "severity": "high",
    },
    
    # Pepper diseases
    {
        "name": "Pepper Bacterial Spot",
        "crop_type": "pepper",
        "description": "Bacterial disease that weakens foliage and fruit quality.",
        "symptoms": "Small water-soaked leaf spots that turn dark and necrotic.",
        "treatment": "Use disease-free seed, avoid overhead irrigation, and apply copper sprays as advised.",
        "severity": "medium",
    },
    {
        "name": "Pepper Anthracnose",
        "crop_type": "pepper",
        "description": "Fungal disease causing fruit rot and yield loss.",
        "symptoms": "Sunken circular lesions on fruit with dark centers and concentric rings.",
        "treatment": "Remove infected fruit, improve air circulation, and apply fungicides during wet periods.",
        "severity": "medium",
    },
    
    # Wheat diseases
    {
        "name": "Wheat Leaf Rust",
        "crop_type": "wheat",
        "description": "Common fungal disease causing orange-brown pustules on leaves.",
        "symptoms": "Small circular to oval orange-brown pustules on leaf surfaces.",
        "treatment": "Plant resistant varieties, apply fungicides at flag leaf stage, and monitor disease pressure.",
        "severity": "high",
    },
    {
        "name": "Wheat Stem Rust",
        "crop_type": "wheat",
        "description": "Devastating fungal disease affecting stems and grain development.",
        "symptoms": "Reddish-brown pustules on stems, leaf sheaths, and heads.",
        "treatment": "Use resistant varieties, apply fungicides early, and destroy volunteer wheat.",
        "severity": "high",
    },
    {
        "name": "Wheat Stripe Rust",
        "crop_type": "wheat",
        "description": "Fungal disease forming yellow stripes on leaves.",
        "symptoms": "Yellow to orange pustules arranged in stripes parallel to leaf veins.",
        "treatment": "Plant resistant varieties, apply fungicides preventively, and scout fields regularly.",
        "severity": "high",
    },
    {
        "name": "Wheat Powdery Mildew",
        "crop_type": "wheat",
        "description": "Fungal disease causing white powdery growth on leaves.",
        "symptoms": "White to gray powdery fungal growth on leaves and stems.",
        "treatment": "Use resistant varieties, ensure good air circulation, and apply fungicides when needed.",
        "severity": "medium",
    },
    {
        "name": "Wheat Fusarium Head Blight",
        "crop_type": "wheat",
        "description": "Fungal disease causing grain contamination and yield loss.",
        "symptoms": "Bleached spikelets, pink-orange fungal growth, shriveled kernels.",
        "treatment": "Plant moderately resistant varieties, apply fungicides at flowering, and avoid corn residue.",
        "severity": "high",
    },
    {
        "name": "Wheat Septoria Leaf Blotch",
        "crop_type": "wheat",
        "description": "Fungal disease causing leaf lesions and reduced photosynthesis.",
        "symptoms": "Irregular brown blotches with yellow halos and black fruiting bodies.",
        "treatment": "Rotate crops, use resistant varieties, and apply fungicides at stem extension.",
        "severity": "medium",
    },
    
    # Soybean diseases
    {
        "name": "Soybean Rust",
        "crop_type": "soybean",
        "description": "Aggressive fungal disease causing rapid defoliation.",
        "symptoms": "Small tan to reddish-brown lesions with raised pustules on lower leaf surface.",
        "treatment": "Scout regularly, apply fungicides preventively, and plant early-maturing varieties.",
        "severity": "high",
    },
    {
        "name": "Soybean Frogeye Leaf Spot",
        "crop_type": "soybean",
        "description": "Fungal disease causing distinctive circular leaf spots.",
        "symptoms": "Circular spots with gray centers and dark reddish-brown borders.",
        "treatment": "Use resistant varieties, rotate crops, and apply fungicides when disease is severe.",
        "severity": "medium",
    },
    {
        "name": "Soybean White Mold",
        "crop_type": "soybean",
        "description": "Fungal disease thriving in cool, moist conditions.",
        "symptoms": "White cottony fungal growth on stems and pods, wilting, and plant death.",
        "treatment": "Improve air circulation, avoid excessive plant density, and apply fungicides at flowering.",
        "severity": "high",
    },
    {
        "name": "Soybean Sudden Death Syndrome",
        "crop_type": "soybean",
        "description": "Soil-borne fungal disease causing root rot and foliar symptoms.",
        "symptoms": "Interveinal chlorosis and necrosis, brown discolored roots, premature defoliation.",
        "treatment": "Use resistant varieties, improve drainage, avoid early planting in cold soil.",
        "severity": "high",
    },
    
    # Cotton diseases
    {
        "name": "Cotton Fusarium Wilt",
        "crop_type": "cotton",
        "description": "Soil-borne fungal disease causing vascular wilting.",
        "symptoms": "Yellowing and wilting of leaves, brown vascular discoloration in stems.",
        "treatment": "Plant resistant varieties, practice long crop rotations, and maintain soil health.",
        "severity": "high",
    },
    {
        "name": "Cotton Verticillium Wilt",
        "crop_type": "cotton",
        "description": "Fungal disease reducing yield and fiber quality.",
        "symptoms": "Yellowing between leaf veins, wilting, and premature defoliation.",
        "treatment": "Use resistant varieties, avoid stress conditions, and manage soil moisture.",
        "severity": "high",
    },
    {
        "name": "Cotton Bacterial Blight",
        "crop_type": "cotton",
        "description": "Bacterial disease affecting leaves and bolls.",
        "symptoms": "Angular water-soaked leaf spots, boll rot, and seedling blight.",
        "treatment": "Use disease-free seed, apply copper bactericides, and practice crop rotation.",
        "severity": "medium",
    },
    
    # Apple diseases
    {
        "name": "Apple Scab",
        "crop_type": "apple",
        "description": "Major fungal disease affecting leaves and fruit.",
        "symptoms": "Olive-green to brown lesions on leaves and fruit, premature leaf drop.",
        "treatment": "Apply fungicides from bud break through summer, use resistant varieties, and remove fallen leaves.",
        "severity": "high",
    },
    {
        "name": "Apple Fire Blight",
        "crop_type": "apple",
        "description": "Bacterial disease causing shoot and branch dieback.",
        "symptoms": "Blackened shoots with shepherd's crook appearance, oozing cankers.",
        "treatment": "Prune infected branches, apply copper or streptomycin sprays, and plant resistant varieties.",
        "severity": "high",
    },
    {
        "name": "Apple Powdery Mildew",
        "crop_type": "apple",
        "description": "Fungal disease affecting new growth and fruit development.",
        "symptoms": "White powdery coating on leaves, shoots, and blossoms.",
        "treatment": "Apply fungicides at pink bud stage, prune to improve air flow, and use resistant varieties.",
        "severity": "medium",
    },
    
    # Grape diseases
    {
        "name": "Grape Powdery Mildew",
        "crop_type": "grape",
        "description": "Common fungal disease affecting all green parts of vine.",
        "symptoms": "White powdery growth on leaves, shoots, and berries.",
        "treatment": "Apply sulfur or fungicides regularly, maintain canopy management, and use resistant varieties.",
        "severity": "high",
    },
    {
        "name": "Grape Downy Mildew",
        "crop_type": "grape",
        "description": "Destructive fungal disease in humid climates.",
        "symptoms": "Yellow oil spots on upper leaf surface, white downy growth below.",
        "treatment": "Apply protective fungicides, improve air circulation, and remove infected leaves.",
        "severity": "high",
    },
    {
        "name": "Grape Black Rot",
        "crop_type": "grape",
        "description": "Fungal disease causing fruit mummification.",
        "symptoms": "Circular brown leaf spots, rotted berries that shrivel into black mummies.",
        "treatment": "Remove mummified fruit, apply fungicides from bloom through veraison, and prune for airflow.",
        "severity": "high",
    },
    
    # Banana diseases
    {
        "name": "Banana Panama Disease",
        "crop_type": "banana",
        "description": "Devastating soil-borne fungal disease causing plant death.",
        "symptoms": "Yellowing of older leaves, splitting of leaf sheaths, wilting, and plant collapse.",
        "treatment": "Use resistant varieties, practice strict sanitation, and avoid moving contaminated soil.",
        "severity": "high",
    },
    {
        "name": "Banana Black Sigatoka",
        "crop_type": "banana",
        "description": "Fungal leaf disease reducing photosynthesis and yield.",
        "symptoms": "Small brown spots enlarging to black streaks with yellow halos.",
        "treatment": "Remove infected leaves, apply fungicides regularly, and improve drainage.",
        "severity": "high",
    },
    
    # Citrus diseases
    {
        "name": "Citrus Greening",
        "crop_type": "citrus",
        "description": "Bacterial disease transmitted by psyllids, devastating to citrus.",
        "symptoms": "Yellow shoots, blotchy mottled leaves, lopsided bitter fruit.",
        "treatment": "Control psyllid vectors, remove infected trees, and use certified disease-free nursery stock.",
        "severity": "high",
    },
    {
        "name": "Citrus Canker",
        "crop_type": "citrus",
        "description": "Bacterial disease causing lesions on fruit, leaves, and stems.",
        "symptoms": "Raised brown lesions with yellow halos on leaves and fruit.",
        "treatment": "Apply copper sprays, prune infected branches, and use windbreaks to reduce spread.",
        "severity": "high",
    },
]


def build_disease_lookup() -> dict[tuple[str, str], dict]:
    return {(entry["crop_type"], entry["name"].lower()): entry for entry in DISEASE_LIBRARY}


def seed_diseases(session) -> None:
    existing = {(d.name, d.crop_type) for d in session.query(Disease.name, Disease.crop_type).all()}

    for entry in DISEASE_LIBRARY:
        key = (entry["name"], entry["crop_type"])
        if key in existing:
            continue
        session.add(
            Disease(
                name=entry["name"],
                crop_type=entry["crop_type"],
                description=entry["description"],
                symptoms=entry["symptoms"],
                treatment=entry["treatment"],
                severity=entry["severity"],
            )
        )
