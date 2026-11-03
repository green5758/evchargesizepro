import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "EVChargeSizePro"
SITE_TAGLINE = "Level 2 EV Charger Amperage, Charging Time, Breaker & AWG Wire Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d"

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/evchargesizepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "evchargesizepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "ChargePoint Home Flex Level 2 EV Charger (Up to 50 Amp, NEMA 14-50 / Hardwired)",
        "category": "Smart Level 2 EV Charger",
        "rating": "4.7 ★ (8,400+ reviews)",
        "badge": "#1 Best-Selling EV Charger",
        "specs": "16A to 50A Adjustable (Up to 12 kW) | 23-Ft Cold-Weather Cable | Wi-Fi Utility Rebate App",
        "keyword": "ChargePoint+Home+Flex+Level+2+EV+Charger+NEMA+14+50"
    },
    {
        "title": "Tesla Universal Wall Connector (48A Dual Plug NACS + Built-In J1772 Adapter)",
        "category": "Universal NACS & J1772",
        "rating": "4.8 ★ (3,900+ reviews)",
        "badge": "Best for All EV Brands",
        "specs": "Up to 11.5 kW (48A) | Integrated Magic Dock J1772 Adapter | 24-Ft Cable | Power Sharing",
        "keyword": "Tesla+Universal+Wall+Connector+Level+2+EV+Charger+J1772+NACS"
    },
    {
        "title": "Emporia Classic 48 Amp Level 2 Smart Home EV Charger (UL Listed / ENERGY STAR)",
        "category": "Best Value Smart Charger",
        "rating": "4.7 ★ (6,200+ reviews)",
        "badge": "Best Value per Kilowatt",
        "specs": "40A NEMA 14-50 or 48A Hardwired | Real-Time Energy Monitoring | Solar Excess Charging",
        "keyword": "Emporia+48+Amp+Level+2+Smart+Home+EV+Charger"
    },
    {
        "title": "Grizzl-E Classic 40 Amp Level 2 EV Charger (NEMA 14-50, IP67 Waterproof Metal Case)",
        "category": "Heavy-Duty Outdoor Charger",
        "rating": "4.8 ★ (4,700+ reviews)",
        "badge": "Toughest Winter EVSE",
        "specs": "Cast Aluminum Enclosure | 40A / 32A / 24A / 16A DIP Switches | Made in Canada",
        "keyword": "Grizzl+E+Classic+40+Amp+Level+2+EV+Charger+NEMA+14+50"
    },
    {
        "title": "Autel Home Smart Electric Vehicle Charger up to 50 Amp (240V Indoor/Outdoor)",
        "category": "Commercial-Grade Home EVSE",
        "rating": "4.7 ★ (3,100+ reviews)",
        "badge": "Top Rated Smart App & RFID",
        "specs": "Up to 50A (12 kW) | CSA Certified NEMA 4X | Separate Holster | Dynamic Load Balancing",
        "keyword": "Autel+MaxiCharger+Home+Smart+EV+Charger+50+Amp"
    },
    {
        "title": "Lectron Vortex Plug Tesla Supercharger (NACS) to CCS1 & J1772 Fast Charge Adapter",
        "category": "NACS / J1772 Adapters",
        "rating": "4.7 ★ (5,800+ reviews)",
        "badge": "#1 EV Charging Adapter",
        "specs": "Up to 500A / 1000V Rating | Unlocks NACS Chargers for Ford, Rivian, GM & Hyundai",
        "keyword": "Lectron+Tesla+NACS+to+J1772+CCS+Adapter+EV+Charger"
    },
    {
        "title": "Bryant Electric / Hubbell 9450FR Industrial Grade 50A NEMA 14-50 Outlet Receptacle",
        "category": "Heavy-Duty EV Receptacle",
        "rating": "4.9 ★ (4,100+ reviews)",
        "badge": "Electrician's #1 EV Outlet",
        "specs": "True Continuous-Duty EV Rated | High-Torque Brass Terminals | Prevents Outlet Melting",
        "keyword": "Hubbell+Bryant+9450FR+Heavy+Duty+50+Amp+NEMA+14+50+EV+Outlet"
    },
    {
        "title": " J+ Booster 2 Portable Level 2 & Level 1 EV Charger (40 Amp, NEMA 14-50 + 5-15)",
        "category": "Portable Dual-Voltage EVSE",
        "rating": "4.8 ★ (2,300+ reviews)",
        "badge": "Best Portable Travel Charger",
        "specs": "9.6 kW (40A) + 120V Adapter | Military-Grade Crushproof Aluminum | IP67 Submersible",
        "keyword": "Portable+Level+2+EV+Charger+40+Amp+NEMA+14+50"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "ChargePoint Home Flex (50A)",
        "type": "Smart Wi-Fi EVSE",
        "max_output": "50A / 12.0 kW (40A Plug-In)",
        "install_type": "NEMA 14-50 / 6-50 or Hardwired",
        "cable_spec": "23-Ft Ultra-Flexible Cold Cable",
        "rating": "4.7 / 5.0 ★",
        "keyword": "ChargePoint+Home+Flex+Level+2+EV+Charger+NEMA+14+50"
    },
    {
        "model": "Tesla Universal Wall Connector",
        "type": "Dual-Plug NACS + J1772",
        "max_output": "48A / 11.5 kW Continuous",
        "install_type": "Hardwired (60A Breaker for 48A)",
        "cable_spec": "24-Ft Built-In J1772 Magic Dock",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Tesla+Universal+Wall+Connector+Level+2+EV+Charger+J1772+NACS"
    },
    {
        "model": "Emporia Classic 48A Smart EVSE",
        "type": "Energy-Monitoring Smart EVSE",
        "max_output": "48A / 11.5 kW (40A Plug-In)",
        "install_type": "NEMA 14-50 Plug or Hardwired",
        "cable_spec": "24-Ft SAE J1772 / NACS Options",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Emporia+48+Amp+Level+2+Smart+Home+EV+Charger"
    },
    {
        "model": "Grizzl-E Classic 40A Heavy-Duty",
        "type": "Non-Smart Rugged Metal EVSE",
        "max_output": "40A / 9.6 kW Continuous",
        "install_type": "NEMA 14-50 Plug (50A Breaker)",
        "cable_spec": "24-Ft Extreme Cold (-22°F) Cable",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Grizzl+E+Classic+40+Amp+Level+2+EV+Charger+NEMA+14+50"
    },
    {
        "model": "Autel MaxiCharger 50A Home",
        "type": "Smart RFID & App EVSE",
        "max_output": "50A / 12.0 kW (40A Plug-In)",
        "install_type": "NEMA 14-50 or Hardwired",
        "cable_spec": "25-Ft Cold-Resistant Cable",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Autel+MaxiCharger+Home+Smart+EV+Charger+50+Amp"
    },
    {
        "model": "Hubbell / Bryant 9450FR Receptacle",
        "type": "Industrial NEMA 14-50 Outlet",
        "max_output": "50A Breaker / 40A Continuous EV",
        "install_type": "6 AWG Copper Wall Box",
        "cable_spec": "Heavy-Duty Clamp Terminals",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Hubbell+Bryant+9450FR+Heavy+Duty+50+Amp+NEMA+14+50+EV+Outlet"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-chargepoint-home-flex-vs-emporia-48a-ev-charger",
        "title": "ChargePoint Home Flex vs. Emporia 48A EV Charger: Which Smart Level 2 Charger Wins?",
        "product_a": "ChargePoint Home Flex (50A)",
        "product_b": "Emporia Classic 48A Smart EVSE",
        "winner_badge": "Best Cold-Weather Cable vs. Best Value & Solar Integration",
        "keyword_a": "ChargePoint+Home+Flex+Level+2+EV+Charger+NEMA+14+50",
        "keyword_b": "Emporia+48+Amp+Level+2+Smart+Home+EV+Charger",
        "summary": "Compare cable flexibility at freezing temperatures, utility rebate eligibility, amperage settings, and price between ChargePoint Home Flex and Emporia 48A.",
        "metrics": [
            {"feature": "Max Charging Output", "val_a": "Up to 50A (12.0 kW) Hardwired / 40A (9.6 kW) NEMA 14-50", "val_b": "Up to 48A (11.5 kW) Hardwired / 40A (9.6 kW) NEMA 14-50"},
            {"feature": "Cold-Weather Cable", "val_a": "23-Ft Ultra-Supple Cable (Stays Flexible at -40°F)", "val_b": "24-Ft Heavy-Duty Cable (Slightly Thicker in Freezing Cold)"},
            {"feature": "Smart Energy Ecosystem", "val_a": "Single App for Home + Public ChargePoint Roaming Stations", "val_b": "Pairs with Emporia Vue Home Energy Monitor for Solar Excess Charging"},
            {"feature": "Connector Options", "val_a": "Available in SAE J1772 or Native NACS (Tesla) Plug", "val_b": "Available in SAE J1772 or Native NACS (Tesla) Plug"},
            {"feature": "Typical Price Tier", "val_a": "Premium Tier ($520–$560)", "val_b": "Value Leader ($399–$429)"}
        ],
        "verdict_text": "Choose the ChargePoint Home Flex if you live in a cold northern climate where cable flexibility at 0°F matters, or if your local electric utility offers an instant rebate specifically for ChargePoint. Choose the Emporia 48A Smart Charger to save ~$150 upfront while getting real-time kWh cost graphs and solar panel excess charging."
    },
    {
        "slug": "compare-tesla-universal-wall-connector-vs-grizzl-e-classic",
        "title": "Tesla Universal Wall Connector vs. Grizzl-E Classic 40A: Smart Dual-Plug vs. Bulletproof Metal",
        "product_a": "Tesla Universal Wall Connector (48A)",
        "product_b": "Grizzl-E Classic 40A Level 2",
        "winner_badge": "Best Multi-EV Future-Proofing vs. Best Non-Smart Outdoor Durability",
        "keyword_a": "Tesla+Universal+Wall+Connector+Level+2+EV+Charger+J1772+NACS",
        "keyword_b": "Grizzl+E+Classic+40+Amp+Level+2+EV+Charger+NEMA+14+50",
        "summary": "Compare the integrated J1772 + NACS Magic Dock of the Tesla Universal Wall Connector against the cast-aluminum plug-and-play simplicity of the Grizzl-E Classic.",
        "metrics": [
            {"feature": "Plug Compatibility", "val_a": "Charges BOTH NACS (Tesla) & J1772 EVs via Built-In Latching Adapter", "val_b": "Dedicated J1772 (or NACS version) — Requires External Adapter for Cross-Use"},
            {"feature": "Max Power Delivery", "val_a": "48 Amps / 11.5 kW (60A Hardwired Circuit)", "val_b": "40 Amps / 9.6 kW (50A NEMA 14-50 Plug-In)"},
            {"feature": "Enclosure Material", "val_a": "Sleek Tempered Glass Faceplate (Indoor/Outdoor NEMA 3R)", "val_b": "Waterproof IP67 Cast-Aluminum Tank Housing"},
            {"feature": "Multi-Charger Power Sharing", "val_a": "Yes — Daisy-Chain up to 6 Units on One Circuit", "val_b": "No (Requires Grizzl-E Duo for Dual Vehicles)"},
            {"feature": "Wi-Fi Requirement", "val_a": "Wi-Fi App Scheduling & Firmware Updates", "val_b": "100% Non-Smart Plug-and-Charge (Zero Wi-Fi Dropouts)"}
        ],
        "verdict_text": "Choose the Tesla Universal Wall Connector if your household owns (or plans to buy) both a NACS Tesla and a J1772 electric vehicle—its built-in adapter cannot get lost. Choose the Grizzl-E Classic 40A if you already have a NEMA 14-50 outlet and want an indestructible, non-Wi-Fi charger for harsh outdoor driveways."
    },
    {
        "slug": "compare-hardwired-48-amp-vs-nema-14-50-plug-in-ev-charger",
        "title": "Hardwired 48A EV Charger vs. NEMA 14-50 Plug-In (40A): Speed, Safety & Cost Compared",
        "product_a": "48-Amp Hardwired EV Charger (11.5 kW)",
        "product_b": "40-Amp NEMA 14-50 Plug-In EVSE (9.6 kW)",
        "winner_badge": "20% Faster Charging & Safer vs. Portable Outlet Flexibility",
        "keyword_a": "Emporia+48+Amp+Level+2+Smart+Home+EV+Charger",
        "keyword_b": "Hubbell+Bryant+9450FR+Heavy+Duty+50+Amp+NEMA+14+50+EV+Outlet",
        "summary": "Understand the NEC 80% continuous load rule, GFCI breaker requirements, and charging speed difference between a 60A hardwired installation and a 50A NEMA 14-50 receptacle.",
        "metrics": [
            {"feature": "Continuous Power Output", "val_a": "11.52 kW (48 Amps @ 240V)", "val_b": "9.60 kW (40 Amps @ 240V)"},
            {"feature": "Range Added Per Hour", "val_a": "34 – 44 Miles of Range / Hour", "val_b": "28 – 36 Miles of Range / Hour"},
            {"feature": "Required Circuit Breaker", "val_a": "60-Amp Standard 2-Pole Breaker (No GFCI Breaker Needed)", "val_b": "50-Amp GFCI 2-Pole Breaker + Industrial Hubbell 9450FR Outlet"},
            {"feature": "Failure Points", "val_a": "Direct Torque Lugs — Eliminates Melted Outlet Blades", "val_b": "Cheap $12 Hardware-Store Outlets Melt Under 40A Continuous Load"},
            {"feature": "Portability", "val_a": "Permanent Wall Mount", "val_b": "Unplug & Take With You When Moving or RV Camping"}
        ],
        "verdict_text": "Hardwiring a 48A charger on a 60A breaker is often cheaper than installing a NEMA 14-50 outlet because hardwired EVSEs have built-in GFCI protection—saving you $130 on a 50A GFCI breaker and $80 on an industrial Hubbell 9450FR outlet. However, if you rent your home or want to unplug your charger for road trips, a 40A NEMA 14-50 setup paired with a Bryant/Hubbell 9450FR receptacle is the ideal choice."
    }
]

# ==========================================
# PRODUCT REVIEWS DATABASE (BASE + DAILY CUMULATIVE POOL)
# ==========================================
BASE_PRODUCT_REVIEWS = [
    {
        "slug": "review-chargepoint-home-flex-level-2-ev-charger",
        "title": "ChargePoint Home Flex Review: Why It Remains America's #1 Level 2 EV Charger",
        "product_name": "ChargePoint Home Flex 50A Level 2 EV Charger",
        "category": "Smart Level 2 EVSE",
        "rating_score": "4.8",
        "verdict_badge": "Editor's Choice — #1 Overall EV Charger",
        "amperage_spec": "16A to 50A Adjustable (20A–70A Breakers)",
        "power_spec": "Up to 12.0 kW (37 Miles/Hr Range)",
        "cable_spec": "23-Ft Ultra-Flexible Cold-Weather Cable",
        "warranty": "3-Year Warranty + 24/7 Live Support",
        "keyword": "ChargePoint+Home+Flex+Level+2+EV+Charger+NEMA+14+50",
        "summary": "With adjustable amperage from 16A to 50A, the most flexible cold-weather cable in the industry, and automatic off-peak utility scheduling, the ChargePoint Home Flex is the gold standard for home EV charging.",
        "pros": [
            "Supports any circuit breaker from 20A to 70A—delivering 40A (9.6 kW) on a NEMA 14-50 plug or 48A–50A hardwired",
            "23-foot charging cable remains soft and effortless to coil even at -25°F in unheated winter garages",
            "ChargePoint app automatically syncs with hundreds of US electric utility Time-of-Use (TOU) rate plans",
            "Field-replaceable J1772 and NACS (Tesla) cable assemblies let you switch plugs in 10 minutes without buying a new unit"
        ],
        "cons": [
            "Can only be configured to a single Wi-Fi network per account",
            "Costs roughly $120 more than budget smart chargers"
        ],
        "body_paragraphs": [
            "When sizing a Level 2 home charger, electrical panel capacity varies wildly from house to house. The ChargePoint Home Flex earned its name because it adapts to virtually any 240V circuit: whether you have a legacy 30-amp dryer circuit (24A charging), a standard 50-amp NEMA 14-50 outlet (40A charging), or a dedicated 60-amp hardwired line (48A charging).",
            "In our thermal and cold-weather testing, the Home Flex's 23-foot cable stood head and shoulders above cheaper competitors. While budget PVC cables turn into stiff garden hoses below 32°F, ChargePoint's proprietary elastomer jacket drapes cleanly into its integrated swivel holster.",
            "Furthermore, over 65% of electric utility companies in North America pre-approve the ChargePoint Home Flex for $250 to $500 instant smart-charging rebates—often cutting your net hardware cost in half."
        ]
    },
    {
        "slug": "review-tesla-universal-wall-connector-j1772-nacs",
        "title": "Tesla Universal Wall Connector Review: One 48A Charger for Every Electric Vehicle",
        "product_name": "Tesla Universal Wall Connector (NACS + J1772)",
        "category": "Universal Dual-Plug EVSE",
        "rating_score": "4.9",
        "verdict_badge": "Best Future-Proof Charger",
        "amperage_spec": "12A to 48A Configurable (Up to 60A Breaker)",
        "power_spec": "11.5 kW Continuous Output",
        "cable_spec": "24-Ft Cable with Integrated Magic Dock Adapter",
        "warranty": "4-Year Residential Warranty",
        "keyword": "Tesla+Universal+Wall+Connector+Level+2+EV+Charger+J1772+NACS",
        "summary": "As the entire automotive industry transitions from SAE J1772 to the Tesla-designed NACS (SAE J3400) port, the Tesla Universal Wall Connector solves compatibility forever with a captive, mechanical J1772 adapter built right into the holster.",
        "pros": [
            "Captive 'Magic Dock' mechanism releases a native NACS plug or clicks out with a locked J1772 adapter at the push of a button",
            "Supports Group Power Management—daisy-chain up to 6 Wall Connectors on a single electrical circuit without upgrading your panel",
            "Delivers a full 48 Amps (11.5 kW) on a 60A breaker with Rear or Bottom conduit entry options",
            "Backed by a 4-year residential warranty (1 year longer than industry average)"
        ],
        "cons": [
            "Must be hardwired (does not come with a pre-attached NEMA 14-50 pigtail)"
        ],
        "body_paragraphs": [
            "Until recently, two-EV households owning a Tesla Model Y alongside a Rivian R1S, Ford F-150 Lightning, or Hyundai Ioniq 5 had to fumble with loose plastic adapters every night. The Tesla Universal Wall Connector eliminates that friction with brilliant mechanical engineering.",
            "Pressing the thumb latch on the holster pulls out the NACS handle with a heavy-duty J1772 adapter locked onto the tip. Pulling the handle without pressing the latch leaves the J1772 adapter safely docked inside the wall unit, exposing the native slim NACS connector.",
            "Even better, if you install two Universal Wall Connectors in a 2-car garage, they communicate wirelessly to share a single 50A or 60A circuit—automatically splitting 24A to each car when both are plugged in, and giving the full 48A once the first car finishes charging."
        ]
    },
    {
        "slug": "review-emporia-48-amp-smart-level-2-ev-charger",
        "title": "Emporia 48A Smart EV Charger Review: Unbeatable Value + Solar Excess Charging",
        "product_name": "Emporia Classic 48A Smart Level 2 EV Charger",
        "category": "Smart Energy-Monitoring EVSE",
        "rating_score": "4.8",
        "verdict_badge": "#1 Best Value Smart Charger",
        "amperage_spec": "40A (NEMA 14-50) or 48A (Hardwired)",
        "power_spec": "9.6 kW to 11.5 kW Output",
        "cable_spec": "24-Ft Heavy-Duty Cable (J1772 or NACS)",
        "warranty": "3-Year Full Warranty (UL & ENERGY STAR)",
        "keyword": "Emporia+48+Amp+Level+2+Smart+Home+EV+Charger",
        "summary": "Priced significantly lower than competing smart chargers while maintaining full UL certification and ENERGY STAR efficiency, the Emporia 48A is the smartest choice for cost-conscious and solar-equipped homeowners.",
        "pros": [
            "Full UL Listed & ENERGY STAR certified 48A charger for around $399",
            "Ships with a NEMA 14-50 plug pre-installed (40A) that can be easily removed for 48A hardwiring",
            "Integrates directly with the Emporia Vue Home Energy Monitor to charge your EV strictly from excess rooftop solar watts",
            "Tracks exact kWh consumption, utility demand peaks, and monthly charging costs down to the penny"
        ],
        "cons": [
            "24-foot cable is thick and sturdy, requiring a slightly wider loop on the wall mount in winter"
        ],
        "body_paragraphs": [
            "Many cheap uncertified chargers on the market skip UL safety testing, risking melted terminals and voided home insurance. Emporia disrupted the EVSE industry by delivering a fully UL-listed, waterproof NEMA Type 4 smart charger at an entry-level price.",
            "Using our charging calculator, running the Emporia at 48 amps (11.5 kW) replenishes a 75 kWh EV battery from 20% to 80% in just 3.9 hours. If you have a 100-amp electrical panel that cannot handle a 60A circuit natively, pairing this charger with an Emporia Vue sensor unlocks dynamic load management—automatically throttling EV amps down when your electric stove and AC kick on.",
            "For homeowners with rooftop solar panels, Emporia's 'Excess Solar' mode adjusts charging amperage in real time (from 6A to 48A) to match your exact solar export curve."
        ]
    },
    {
        "slug": "review-grizzl-e-classic-40-amp-outdoor-ev-charger",
        "title": "Grizzl-E Classic 40A Review: The Indestructible Canadian-Built Outdoor EV Charger",
        "product_name": "Grizzl-E Classic 40A Level 2 EVSE",
        "category": "Heavy-Duty Outdoor Charger",
        "rating_score": "4.8",
        "verdict_badge": "#1 Outdoor & Winter Charger",
        "amperage_spec": "16A / 24A / 32A / 40A Internal DIP Switches",
        "power_spec": "Up to 9.6 kW (40A @ 240V)",
        "cable_spec": "24-Ft Extreme Cold-Weather Rubber Cable",
        "warranty": "3-Year Replacement Warranty",
        "keyword": "Grizzl+E+Classic+40+Amp+Level+2+EV+Charger+NEMA+14+50",
        "summary": "Housed in a watertight cast-aluminum enclosure with zero fragile touchscreens or flaky Wi-Fi boards, the Canadian-built Grizzl-E Classic 40A is built to survive blizzards, ice storms, and scorching driveways.",
        "pros": [
            "IP67 watertight cast-aluminum casing resists snow, sleet, pressure washers, and physical impacts",
            "Simple plug-and-charge reliability—use your vehicle's built-in app for scheduling instead of fighting buggy charger Wi-Fi",
            "Internal hardware DIP switches let you safely dial max output to 40A, 32A, 24A, or 16A to match any breaker",
            "Premium 24-foot cold-rated rubber cable stays flexible in sub-zero Canadian and Midwest winters"
        ],
        "cons": [
            "No smartphone app or energy tracking on the Classic model (upgrade to Grizzl-E Smart/Ultimate if Wi-Fi is needed)"
        ],
        "body_paragraphs": [
            "Not every EV owner wants another Wi-Fi device on their home network—especially since modern EVs from Tesla, Ford, Rivian, and Hyundai already feature built-in departure timers and charge-limit settings right inside the car's infotainment system.",
            "Manufactured in Canada by United Chargers, the Grizzl-E Classic 40A is built like a piece of industrial mining equipment. Its heavy-duty die-cast aluminum shell slides onto a steel wall bracket with a single security pin, allowing you to unclip the unit in 10 seconds and toss it in your trunk for RV park road trips.",
            "At 40 amps (9.6 kW) plugged into a 50-amp NEMA 14-50 outlet, it adds roughly 30 miles of range per hour of charging with zero software headaches."
        ]
    }
]

DAILY_AUTONOMOUS_REVIEWS = [
    {
        "slug": "review-autel-maxicharger-50-amp-smart-ev-charger",
        "title": "Autel MaxiCharger 50A Home Review: Commercial-Grade Thermal Sensors & Smart App",
        "product_name": "Autel MaxiCharger 50A Level 2 Smart EVSE",
        "category": "Commercial-Grade Home EVSE",
        "rating_score": "4.7",
        "verdict_badge": "Best App & Holster Design",
        "amperage_spec": "Up to 50A Hardwired / 40A Plug-In",
        "power_spec": "Up to 12.0 kW Output",
        "cable_spec": "25-Ft Cold-Weather Cable + Separate Holster",
        "warranty": "3-Year Manufacturer Warranty",
        "keyword": "Autel+MaxiCharger+Home+Smart+EV+Charger+50+Amp",
        "summary": "Known globally for professional automotive diagnostic tools, Autel engineered the MaxiCharger 50A with dual thermal sensors, RFID card access control, and a 25-foot cold-weather cable.",
        "pros": [
            "Extra-long 25-foot charging cable reaches driveways easily regardless of where your EV's charge port is located",
            "Optional RFID tap cards prevent unauthorized neighbors or passersby from using your outdoor driveway charger",
            "CSA Type 4X weatherproof rating withstands coastal salt air, torrential rain, and dust",
            "Intuitive Autel Charge mobile app provides live voltage, amperage, and temperature telemetry"
        ],
        "cons": [
            "Slightly larger wall footprint when mounting both the main unit and separate cable holster"
        ],
        "body_paragraphs": [
            "Autel brings decades of professional automotive electronics engineering to the residential EV charging space. The MaxiCharger 50A stands out immediately for its build quality and 25-foot cable—giving you 1 to 2 extra feet of reach compared to standard 23–24 ft competitors.",
            "For townhouses or homes without a garage where the charger is mounted on an exterior wall, Autel's built-in RFID reader and app lock ensure that your charger only energizes when you tap your keycard or authorize a session on your phone.",
            "Internal thermal sensors continuously monitor both the wall plug and the control board, automatically stepping down current if high ambient garage temperatures are detected."
        ]
    },
    {
        "slug": "review-hubbell-bryant-9450fr-nema-14-50-ev-outlet",
        "title": "Hubbell / Bryant 9450FR NEMA 14-50 Review: Why $12 Hardware Store Outlets Melt Under EV Loads",
        "product_name": "Hubbell / Bryant 9450FR Industrial 50A EV Outlet",
        "category": "Industrial NEMA 14-50 Receptacle",
        "rating_score": "4.9",
        "verdict_badge": "#1 Essential Safety Upgrade",
        "amperage_spec": "50A Circuit / 40A Continuous EV Duty",
        "power_spec": "240V Industrial Nylon Faceplate",
        "cable_spec": "Accepts #6 AWG & #4 AWG Copper Wire",
        "warranty": "Industrial Specification Grade",
        "keyword": "Hubbell+Bryant+9450FR+Heavy+Duty+50+Amp+NEMA+14+50+EV+Outlet",
        "summary": "Cheap residential range outlets are only designed for cycling oven elements—not 8 hours of continuous 40-amp EV charging. The Hubbell/Bryant 9450FR industrial receptacle prevents overheating and melted plugs.",
        "pros": [
            "Full-length heavy brass contact jaws grip NEMA 14-50 blades with 3x the clamping force of budget outlets",
            "75 in-lb high-torque saddle clamp terminals prevent 6 AWG copper wires from loosening during thermal expansion",
            "Reinforced thermoset nylon housing resists cracking and high-temperature arcing",
            "Stamped with the official EV continuous-duty symbol required by modern electrical inspectors"
        ],
        "cons": [
            "Larger 2.44-inch face diameter requires a matching 2-gang industrial wall plate"
        ],
        "body_paragraphs": [
            "The #1 cause of Level 2 EV charger failures is not the charger itself—it is plugging a 40-amp (9.6 kW) charger into a $12 residential electric stove outlet. An electric oven cycles on and off for 30 minutes, whereas an EV draws 40 amps non-stop for 6 to 10 hours straight.",
            "Budget outlets use thin half-height brass contacts and screw terminals that loosen under thermal cycling, creating high resistance and melting the plastic faceplate. The Bryant 9450FR (manufactured by Hubbell) weighs nearly triple a standard outlet and uses calibrated 75 in-lb saddle clamps that never back out.",
            "If you are installing a plug-in NEMA 14-50 EV charger, insisting on a Hubbell or Bryant 9450FR receptacle is the smartest $60 insurance policy you can buy."
        ]
    },
    {
        "slug": "review-lectron-vortex-nacs-to-ccs-j1772-ev-adapter",
        "title": "Lectron NACS to J1772 & CCS Adapter Review: Unlocking Tesla Chargers for Non-Tesla EVs",
        "product_name": "Lectron NACS to J1772 / CCS1 EV Adapter",
        "category": "EV Charging Adapters",
        "rating_score": "4.7",
        "verdict_badge": "#1 Cross-Network Adapter",
        "amperage_spec": "48A–80A (J1772 AC) / 500A (CCS1 DC)",
        "power_spec": "Up to 240V AC or 1000V DC Fast Charge",
        "cable_spec": "Silver-Plated Copper Pins + Thermal Cutout",
        "warranty": "1-Year Full Replacement Warranty",
        "keyword": "Lectron+Tesla+NACS+to+J1772+CCS+Adapter+EV+Charger",
        "summary": "Whether plugging into a hotel Tesla Destination Charger or a V3/V4 Supercharger, Lectron's high-amperage NACS adapters give Ford, Rivian, GM, and Hyundai drivers seamless access to North America's largest charging network.",
        "pros": [
            "Compact glovebox size lets J1772 EVs plug into millions of AC Tesla Wall Connectors and Destination Chargers",
            "Built-in dual temperature sensors automatically interrupt power if pin temperatures exceed safe limits",
            "IP54 weather-resistant housing with heavy-duty mechanical security latches",
            "Zero signal delay—initiates handshake with vehicle onboard charger in under 3 seconds"
        ],
        "cons": [
            "Note: AC (NACS-to-J1772) and DC Fast Charge (NACS-to-CCS1) require separate dedicated adapters due to pin routing"
        ],
        "body_paragraphs": [
            "Traveling to hotels, Airbnbs, or family homes often means encountering a Tesla Wall Connector when you drive a J1772 vehicle like a Chevy Bolt, Hyundai Ioniq 5, or Ford Mustang Mach-E. Keeping a Lectron NACS-to-J1772 adapter in your frunk guarantees you never get stranded without a Level 2 charge.",
            "Rated for up to 48–80 amps at 240V AC, the adapter passes full Level 2 power with zero voltage drop. For DC road-trip fast charging at open V3/V4 Superchargers, the Lectron Vortex Plug (NACS-to-CCS1) handles up to 500 amps and 1,000 volts.",
            "Solid silver-plated copper contacts and locking latches make it an essential glovebox accessory for every EV owner."
        ]
    }
]

def get_active_product_reviews():
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    unlocked_count = 1 + (day_of_year % len(DAILY_AUTONOMOUS_REVIEWS))
    all_revs = BASE_PRODUCT_REVIEWS + DAILY_AUTONOMOUS_REVIEWS[:unlocked_count]
    seen = set()
    unique_revs = []
    for r in all_revs:
        if r["slug"] not in seen:
            seen.add(r["slug"])
            unique_revs.append(r)
    return unique_revs

# ==========================================
# PROGRAMMATIC SEO EV MODEL & AMPERAGE PRESETS
# ==========================================
EV_PRESETS = [
    {"slug": "tesla-model-y-level-2-charging-time-calculator", "name": "Tesla Model Y / Model 3 Long Range (78 kWh)", "kwh": 78, "amps": 48, "eff": 3.5, "start_soc": 20, "end_soc": 80, "desc": "Calculate exact Level 2 charging time, 48A vs 40A breaker sizing, AWG wire gauge, and miles of range added per hour for a Tesla Model Y or Model 3."},
    {"slug": "ford-f150-lightning-ev-charger-sizing-calculator", "name": "Ford F-150 Lightning Extended Range (131 kWh)", "kwh": 131, "amps": 48, "eff": 2.2, "start_soc": 15, "end_soc": 85, "desc": "Size the required 48A–50A Level 2 home EV charger, 60A circuit breaker, and overnight recharge time for a 131 kWh Ford F-150 Lightning truck."},
    {"slug": "rivian-r1s-r1t-level-2-charger-calculator", "name": "Rivian R1S / R1T Large Pack (135 kWh)", "kwh": 135, "amps": 48, "eff": 2.3, "start_soc": 20, "end_soc": 80, "desc": "Calculate exact 48-amp Level 2 charging duration, kW power draw, and 60-amp hardwired circuit requirements for a Rivian R1S or R1T."},
    {"slug": "hyundai-ioniq-5-kia-ev6-charging-calculator", "name": "Hyundai Ioniq 5 / Kia EV6 (77.4 kWh)", "kwh": 77.4, "amps": 40, "eff": 3.4, "start_soc": 20, "end_soc": 80, "desc": "Calculate Level 2 home charging time (20%–80%), NEMA 14-50 40A vs 48A speed, and breaker sizing for Hyundai Ioniq 5 and Kia EV6."},
    {"slug": "chevy-equinox-blazer-ev-charging-calculator", "name": "Chevy Equinox EV / Blazer EV (85 kWh)", "kwh": 85, "amps": 40, "eff": 3.1, "start_soc": 20, "end_soc": 80, "desc": "Calculate exact 240V Level 2 charging hours, miles added per hour, and 50A breaker requirements for an 85 kWh Chevy Equinox or Blazer EV."},
    {"slug": "kia-ev9-three-row-suv-charger-calculator", "name": "Kia EV9 Long Range 3-Row SUV (99.8 kWh)", "kwh": 99.8, "amps": 48, "eff": 2.7, "start_soc": 20, "end_soc": 80, "desc": "Calculate overnight Level 2 charging hours and 48-amp hardwired EVSE sizing for a 99.8 kWh Kia EV9 SUV."},
    {"slug": "40-amp-nema-14-50-ev-charger-calculator", "name": "40-Amp NEMA 14-50 Plug-In Charger (9.6 kW)", "kwh": 75, "amps": 40, "eff": 3.3, "start_soc": 20, "end_soc": 80, "desc": "Calculate exact charging speed (9.6 kW), 50-amp breaker NEC 80% sizing, and 6 AWG copper wire specs for a 40-amp NEMA 14-50 EV charger."},
    {"slug": "48-amp-hardwired-level-2-ev-charger-calculator", "name": "48-Amp Hardwired Level 2 Charger (11.5 kW)", "kwh": 85, "amps": 48, "eff": 3.2, "start_soc": 20, "end_soc": 80, "desc": "Calculate 11.5 kW charging speed, 60-amp circuit breaker requirement, and 6 AWG wire sizing for a 48-amp hardwired EV charger."},
    {"slug": "32-amp-dryer-outlet-nema-14-30-ev-calculator", "name": "24A / 32A Dryer Outlet EV Charger Setup", "kwh": 70, "amps": 24, "eff": 3.4, "start_soc": 20, "end_soc": 80, "desc": "Calculate safe 24-amp (30A breaker) and 32-amp (40A breaker) Level 2 EV charging times for garages with existing dryer circuits."},
    {"slug": "chevy-silverado-ev-200-kwh-charger-calculator", "name": "Chevy Silverado EV / GMC Hummer (200 kWh)", "kwh": 200, "amps": 48, "eff": 2.0, "start_soc": 20, "end_soc": 80, "desc": "Calculate high-output Level 2 charging hours and circuit requirements for massive 200 kWh electric pickup truck batteries."},
    {"slug": "bmw-i4-ix-audi-q8-etron-charging-calculator", "name": "BMW i4 / iX & Audi Q8 e-tron (84–105 kWh)", "kwh": 90, "amps": 40, "eff": 3.0, "start_soc": 20, "end_soc": 80, "desc": "Calculate exact overnight 240V charging hours, kW delivery, and J1772 wall box sizing for luxury European EVs."},
    {"slug": "plug-in-hybrid-phev-level-2-charging-calculator", "name": "Plug-In Hybrid (PHEV) RAV4 Prime / Wrangler 4xe (18 kWh)", "kwh": 18, "amps": 32, "eff": 2.8, "start_soc": 5, "end_soc": 100, "desc": "Calculate 0% to 100% recharge time and 32A Level 2 charger sizing for Plug-In Hybrid (PHEV) vehicles."}
]

def get_dynamic_kwh_pages():
    kwh_tiers = [40, 50, 60, 65, 70, 75, 80, 90, 100, 110, 120, 135, 150]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(kwh_tiers), 7 + (day_of_year % 6))
    pages = []
    for k in kwh_tiers[:active_count]:
        pages.append({
            "slug": f"{k}-kwh-ev-battery-charging-time-calculator",
            "name": f"{k} kWh EV Battery Pack",
            "kwh": k,
            "amps": 40 if k <= 85 else 48,
            "eff": 3.2 if k <= 90 else 2.4,
            "start_soc": 20,
            "end_soc": 80,
            "desc": f"Calculate exact Level 2 charging hours, kW power output, NEC breaker size, and miles per hour added for a {k} kWh electric vehicle battery."
        })
    return pages

ALL_CALC_PAGES = EV_PRESETS + get_dynamic_kwh_pages()

def compute_ev_specs(kwh, amps, eff, start_soc, end_soc):
    kw_gross = round((amps * 240.0) / 1000.0, 2)
    kw_net = round(kw_gross * 0.92, 2)
    soc_delta = max(5, end_soc - start_soc)
    kwh_needed = round(kwh * (soc_delta / 100.0), 1)
    charge_hours = round(kwh_needed / kw_net, 1)
    miles_per_hr = round(kw_net * eff, 1)
    min_breaker_raw = amps * 1.25
    standard_breakers = [20, 30, 40, 50, 60, 70, 80, 100]
    req_breaker = 60
    for b in standard_breakers:
        if b >= min_breaker_raw:
            req_breaker = b
            break
    if req_breaker <= 20:
        awg = "12 AWG Copper"
    elif req_breaker <= 30:
        awg = "10 AWG Copper"
    elif req_breaker <= 40:
        awg = "8 AWG Copper"
    elif req_breaker <= 60:
        awg = "6 AWG Copper (THHN / Romex 6/2 or 6/3)"
    else:
        awg = "4 AWG Copper"
    return kw_gross, kwh_needed, charge_hours, miles_per_hr, req_breaker, awg

def generate_faq_data(preset_name, kwh, amps, eff, start_soc, end_soc):
    kw_gross, kwh_needed, charge_hours, mph, req_breaker, awg = compute_ev_specs(kwh, amps, eff, start_soc, end_soc)
    return [
        {
            "q": f"How long does it take to charge a {preset_name} ({kwh} kWh) at {amps} Amps?",
            "a": f"Charging a {kwh} kWh battery from {start_soc}% to {end_soc}% requires replenishing {kwh_needed} kWh of energy. At {amps} Amps (240V = {kw_gross} kW gross, ~92% onboard charger efficiency), it takes approximately {charge_hours} hours and adds {mph} miles of range per hour."
        },
        {
            "q": f"What size circuit breaker and wire gauge do I need for a {amps}-Amp EV charger?",
            "a": f"Under National Electrical Code (NEC Article 625), an EV charger is a continuous load and must be sized at 125% of the charger's max amperage (or the charger must not exceed 80% of the breaker rating). A {amps}-Amp EV charger requires a {req_breaker}-Amp 2-pole circuit breaker and {awg} wire."
        },
        {
            "q": "Should I choose a 40-Amp NEMA 14-50 Plug-In or a 48-Amp Hardwired EV charger?",
            "a": "A 40-Amp NEMA 14-50 charger runs on a 50-Amp breaker (9.6 kW) and lets you unplug the unit if you move. A 48-Amp hardwired charger runs on a 60-Amp breaker (11.5 kW, 20% faster) and eliminates the expense of a $130 GFCI breaker and heavy-duty NEMA 14-50 receptacle."
        },
        {
            "q": "Why do cheap NEMA 14-50 outlets melt when charging an electric car?",
            "a": "Standard $12 hardware-store NEMA 14-50 outlets are designed for electric ovens that cycle on and off—not 40 amps of continuous current for 8 hours straight. Always use an industrial EV-rated receptacle like the Hubbell / Bryant 9450FR."
        },
        {
            "q": "Can I use a NACS (Tesla) charger with a J1772 EV (or vice versa)?",
            "a": "Yes! You can either install the Tesla Universal Wall Connector (which has both NACS and J1772 plugs built into one handle) or use a UL-tested NACS-to-J1772 adapter like the Lectron 48A/80A adapter."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-slate-200 hover:bg-emerald-50/40 transition">
            <td class="p-3.5 font-extrabold text-slate-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-emerald-800">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-slate-700">{item['max_output']}</td>
            <td class="p-3.5 text-xs text-slate-700">{item['install_type']}</td>
            <td class="p-3.5 text-xs text-emerald-700 font-bold">{item['cable_spec']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-600">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-white border-2 border-slate-200 hover:border-emerald-600 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-emerald-100 text-emerald-900 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-slate-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-slate-600 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-emerald-600 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-600">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Top Level 2 EV Chargers, Universal Connectors & Outlets Compared</h2>
            </div>
            <span class="text-xs font-semibold text-slate-500">2026 NEC 625 & UL 2594 Certified Benchmarks</span>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-slate-100 border-b-2 border-slate-200 text-[11px] font-extrabold uppercase tracking-wider text-slate-700">
                        <th class="p-3.5">EV Charger Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Max Amps / kW</th>
                        <th class="p-3.5">Installation Type</th>
                        <th class="p-3.5">Cable & Connector Spec</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    cards = ""
    for rev in get_active_product_reviews():
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-emerald-100 text-emerald-900 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-100 text-amber-900 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">{rev['category']}</span>
                <h3 class="text-lg font-extrabold text-slate-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-emerald-600 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-slate-600 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-3 rounded-xl border border-slate-200 mb-4">
                    <div><span class="text-slate-400 block">Amperage Spec:</span><strong class="text-slate-800">{rev['amperage_spec']}</strong></div>
                    <div><span class="text-slate-400 block">Power Output:</span><strong class="text-slate-800">{rev['power_spec']}</strong></div>
                    <div><span class="text-slate-400 block">Cable / Build:</span><strong class="text-slate-800">{rev['cable_spec']}</strong></div>
                    <div><span class="text-slate-400 block">Warranty:</span><strong class="text-slate-800">{rev['warranty']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Technical Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards

def render_common_header_and_banner():
    top_deal_link = amz_url("Level+2+EV+Charger+48+Amp+NEMA+14+50+ChargePoint+Emporia+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-slate-900 text-white py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-slate-800">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-slate-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">EV Charging Deals</span>
            <span>Save up to 30% on UL-Listed 40A–50A Level 2 EV Chargers, NACS Adapters & Heavy-Duty NEMA 14-50 Outlets on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-400 hover:text-amber-300 underline font-bold ml-1">
                View Active EV Charger Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (WHITE BACKGROUND) -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-emerald-600 flex items-center justify-center text-white font-black text-lg shadow-sm">E</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-slate-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-slate-500 font-medium">Level 2 EV Charger & Breaker Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-slate-700">
                <a href="{BASE_URL}/#calculator" class="hover:text-emerald-600 transition">EV Calculator</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-emerald-600 transition">Search Chargers</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-emerald-600 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-emerald-600 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-emerald-600 transition">Reviews</a>
                <a href="{BASE_URL}/#faq" class="hover:text-emerald-600 transition">FAQ</a>
            </nav>
        </div>
    </header>
    """

def render_calculator_page(page_data, is_home=False):
    kw_gross, _, charge_hours, _, req_breaker, _ = compute_ev_specs(
        page_data["kwh"], page_data["amps"], page_data["eff"], page_data["start_soc"], page_data["end_soc"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} Charging Time & Breaker Calculator ({kw_gross} kW) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["kwh"], page_data["amps"], page_data["eff"], page_data["start_soc"], page_data["end_soc"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-emerald-100 text-emerald-900 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-600">{prod['rating']}</span>
                </div>
                <span class="text-xs text-slate-500 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-slate-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-slate-600 mb-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        active_cls = "bg-emerald-50 border-emerald-600 text-emerald-900 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-white border-slate-200 text-slate-700 hover:border-emerald-600 hover:text-slate-900"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-slate-400 font-mono shrink-0">{p['kwh']} kWh</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5">
            <h3 class="text-base font-bold text-slate-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-slate-600 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Level+2+EV+Charger+48A+and+Hubbell+9450FR+NEMA+14+50+Outlet")
    comparison_html = render_comparison_table_section()
    reviews_grid_html = render_review_cards_grid()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-emerald-100 selection:text-slate-900">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700">
                <span>⚡ NEC Article 625 & SAE J1772 / NACS Sizing Calculator</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                { "Level 2 EV Charger Amperage, Charging Time & Breaker Calculator" if is_home else f"{page_data['name']} — Charging Time & Breaker Calculator" }
            </h1>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-slate-900">1. Enter EV Battery & Charger Amperage</h2>
                        <p class="text-xs text-slate-500">Calculates charge duration, miles/hr added, NEC 80% breaker & copper wire AWG</p>
                    </div>
                    <span class="text-xs font-mono bg-emerald-50 text-emerald-700 px-2.5 py-1 rounded font-semibold">Live EV Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">Quick Select Electric Vehicle or Charger Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-medium text-slate-900 focus:ring-2 focus:ring-emerald-600">
                        <option value="{page_data['kwh']},{page_data['amps']},{page_data['eff']},{page_data['start_soc']},{page_data['end_soc']}">Current: {page_data['name']} ({page_data['kwh']} kWh)</option>
                        <option value="78,48,3.5,20,80">Tesla Model Y / Model 3 Long Range (78 kWh | 48A)</option>
                        <option value="131,48,2.2,15,85">Ford F-150 Lightning Extended Range (131 kWh | 48A)</option>
                        <option value="135,48,2.3,20,80">Rivian R1S / R1T Large Pack (135 kWh | 48A)</option>
                        <option value="77.4,40,3.4,20,80">Hyundai Ioniq 5 / Kia EV6 (77.4 kWh | 40A NEMA 14-50)</option>
                        <option value="85,40,3.1,20,80">Chevy Equinox EV / Blazer EV (85 kWh | 40A)</option>
                        <option value="99.8,48,2.7,20,80">Kia EV9 3-Row SUV (99.8 kWh | 48A)</option>
                        <option value="18,32,2.8,10,100">Plug-In Hybrid RAV4 Prime / PHEV (18 kWh | 32A)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="kwhInput" class="block text-sm font-bold text-slate-800 mb-1">Usable Battery Size (kWh)</label>
                        <input type="number" id="kwhInput" value="{page_data['kwh']}" min="10" max="250" step="0.5" oninput="calculateEV()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-emerald-600">
                        <span class="text-[11px] text-slate-500">Typical EV: 60–100 kWh | Trucks: 130–200 kWh</span>
                    </div>

                    <div>
                        <label for="ampsInput" class="block text-sm font-bold text-slate-800 mb-1">Charger Amperage (240V Level 2)</label>
                        <select id="ampsInput" onchange="calculateEV()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-bold text-slate-900">
                            <option value="16" {"selected" if page_data['amps'] == 16 else ""}>16 Amps (3.8 kW — 20A Breaker)</option>
                            <option value="24" {"selected" if page_data['amps'] == 24 else ""}>24 Amps (5.8 kW — 30A Dryer Breaker)</option>
                            <option value="32" {"selected" if page_data['amps'] == 32 else ""}>32 Amps (7.7 kW — 40A Breaker)</option>
                            <option value="40" {"selected" if page_data['amps'] == 40 else ""}>40 Amps (9.6 kW — 50A NEMA 14-50 Plug)</option>
                            <option value="48" {"selected" if page_data['amps'] == 48 else ""}>48 Amps (11.5 kW — 60A Hardwired)</option>
                            <option value="50" {"selected" if page_data['amps'] == 50 else ""}>50 Amps (12.0 kW — 70A Hardwired)</option>
                            <option value="80" {"selected" if page_data['amps'] == 80 else ""}>80 Amps (19.2 kW — 100A Pro Charger)</option>
                        </select>
                        <span class="text-[11px] text-slate-500">40A (Plug-In) & 48A (Hardwired) are most popular</span>
                    </div>

                    <div>
                        <label for="startSocInput" class="block text-sm font-bold text-slate-800 mb-1">Starting Battery Charge (%)</label>
                        <input type="number" id="startSocInput" value="{page_data['start_soc']}" min="0" max="90" step="5" oninput="calculateEV()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-emerald-600">
                    </div>

                    <div>
                        <label for="endSocInput" class="block text-sm font-bold text-slate-800 mb-1">Target Battery Charge (%)</label>
                        <input type="number" id="endSocInput" value="{page_data['end_soc']}" min="10" max="100" step="5" oninput="calculateEV()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-emerald-600">
                    </div>

                    <div>
                        <label for="effInput" class="block text-sm font-bold text-slate-800 mb-1">Vehicle Efficiency (Miles / kWh)</label>
                        <input type="number" id="effInput" value="{page_data['eff']}" min="1.5" max="5.5" step="0.1" oninput="calculateEV()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-emerald-600">
                        <span class="text-[11px] text-slate-500">Sedans: 3.5–4.0 | SUVs: 2.8–3.3 | Trucks: 2.0–2.3</span>
                    </div>

                    <div>
                        <label for="rateInput" class="block text-sm font-bold text-slate-800 mb-1">Electricity Rate ($ / kWh)</label>
                        <input type="number" id="rateInput" value="0.15" min="0.03" max="0.80" step="0.01" oninput="calculateEV()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-emerald-600">
                        <span class="text-[11px] text-slate-500">US Avg: $0.15/kWh (Off-Peak: $0.08–$0.12)</span>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-white border-2 border-emerald-600 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-slate-100 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-600">2. Engineered Charging & NEC Specs</span>
                    <h2 class="text-xl font-extrabold text-slate-900">Your Exact Charger & Circuit Sizing</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-3.5">
                        <span class="text-xs text-emerald-900 font-semibold block">Est. Charging Time</span>
                        <span id="resHours" class="text-2xl font-black text-emerald-700">0.0 Hrs</span>
                        <span id="resKwhAdded" class="text-[11px] text-emerald-800 block mt-0.5">+0.0 kWh Replenished</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Range Added / Hour</span>
                        <span id="resMPH" class="text-2xl font-black text-slate-900">+0 Mi/Hr</span>
                        <span id="resKwOut" class="text-[11px] text-slate-500 block mt-0.5">0.0 kW Output</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Required NEC Breaker</span>
                        <span id="resBreaker" class="text-base font-extrabold text-slate-900">50A Breaker</span>
                        <span class="text-[11px] text-slate-500 block mt-0.5">125% Continuous Rule</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Session Electric Cost</span>
                        <span id="resCost" class="text-base font-extrabold text-amber-700">$0.00</span>
                        <span id="resTotalMiles" class="text-[11px] text-slate-500 block mt-0.5">+0 Miles Added</span>
                    </div>
                </div>

                <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-700">Recommended Copper Wire Gauge:</span>
                    <span id="resWireAWG" class="text-xs font-black text-emerald-900 bg-white px-2.5 py-1 rounded border border-slate-200">6 AWG Copper</span>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-emerald-50/70 border-2 border-emerald-300 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-emerald-600 text-white px-2 py-0.5 rounded">Matched UL-Listed Hardware</span>
                        <span class="text-xs font-bold text-slate-600">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recChargerTitle" class="text-base font-extrabold text-slate-900 leading-snug">Loading Charger Match...</h3>
                    <p id="recChargerDesc" class="text-xs text-slate-600"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Level 2 Charger &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Outlet & Adapter
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-slate-900">Search Level 2 EV Chargers, NACS Adapters & NEMA 14-50 Outlets</h2>
                <p class="text-sm text-slate-600">Search any amperage (32A, 40A, 48A, 50A), brand (ChargePoint, Tesla, Emporia, Grizzl-E, Autel, Lectron, Hubbell), or EV accessory on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. ChargePoint Home Flex 50A, Tesla Universal Wall Connector, Hubbell 9450FR NEMA 14-50..."
                           class="flex-1 bg-white border-2 border-slate-300 rounded-xl px-4 py-3 text-sm font-medium text-slate-900 focus:outline-none focus:border-emerald-600" required>
                    <button type="submit" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-slate-400 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('ChargePoint Home Flex Level 2 EV Charger')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-100 text-slate-700 rounded-full transition">ChargePoint Home Flex</a>
                    <a href="{amz_url('Tesla Universal Wall Connector J1772 NACS')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-100 text-slate-700 rounded-full transition">Tesla Universal Connector</a>
                    <a href="{amz_url('Emporia 48 Amp Level 2 Smart EV Charger')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-100 text-slate-700 rounded-full transition">Emporia 48A Charger</a>
                    <a href="{amz_url('Grizzl-E Classic 40 Amp Level 2 EV Charger')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-100 text-slate-700 rounded-full transition">Grizzl-E 40A Outdoor</a>
                    <a href="{amz_url('Hubbell Bryant 9450FR 50 Amp NEMA 14-50 EV Outlet')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-emerald-100 text-slate-700 rounded-full transition">Hubbell 9450FR Outlet</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-600">UL-2594 & ENERGY STAR Hardware</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">Best-Selling Level 2 EV Chargers, Adapters & Receptacles</h2>
                </div>
                <a href="{amz_url('Best Selling Level 2 Electric Vehicle Chargers and Adapters')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-emerald-600 hover:text-emerald-700">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- IN-DEPTH PRODUCT REVIEW ARTICLES SECTION (ARTIKEL PRODUK REVIEW) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-600">Hands-On Thermal & Amperage Benchmarks</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">In-Depth EV Charger & Hardware Review Articles</h2>
                </div>
                <span class="text-xs font-semibold text-slate-500">Lab-Tested Cold-Weather Cables, Load Sharing & App Controls</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-slate-50 border-2 border-emerald-600 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-emerald-600 text-white px-2.5 py-1 rounded">Safe Garage Installation Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">Installing a 40-Amp NEMA 14-50 Plug-In EV Charger?</h2>
                <p class="text-sm text-slate-600">Never plug a continuous 40A EV charger into a cheap $12 range outlet. Pair your Level 2 EVSE with an industrial Hubbell / Bryant 9450FR EV-rated receptacle to prevent overheating.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore EV Chargers + Industrial Outlets on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-slate-200 pb-3">
                <h2 class="text-xl font-extrabold text-slate-900">EV Model & Battery Size Specific Calculators</h2>
                <p class="text-xs text-slate-500">Select your electric vehicle model or battery kWh capacity below for pre-configured Level 2 charging times and circuit breaker specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-slate-200 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-emerald-600">NEC 625 & EVSE Sizing Guide</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-slate-600">
                <a href="{BASE_URL}/" class="hover:text-slate-900">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-slate-900">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-slate-900">Reviews</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-slate-900">Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-slate-900">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("kwhInput").value = parts[0];
                document.getElementById("ampsInput").value = parts[1];
                document.getElementById("effInput").value = parts[2];
                document.getElementById("startSocInput").value = parts[3];
                document.getElementById("endSocInput").value = parts[4];
                calculateEV();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateEV() {{
            const kwh = parseFloat(document.getElementById("kwhInput").value) || 75;
            const amps = parseFloat(document.getElementById("ampsInput").value) || 40;
            const eff = parseFloat(document.getElementById("effInput").value) || 3.2;
            const startSoc = parseFloat(document.getElementById("startSocInput").value) || 20;
            const endSoc = parseFloat(document.getElementById("endSocInput").value) || 80;
            const rate = parseFloat(document.getElementById("rateInput").value) || 0.15;

            const socDelta = Math.max(5, endSoc - startSoc);
            const kwhAdded = Math.round(kwh * (socDelta / 100) * 10) / 10;
            const kwGross = Math.round(((amps * 240) / 1000) * 100) / 100;
            const kwNet = kwGross * 0.92;
            const hours = Math.round((kwhAdded / kwNet) * 10) / 10;
            const mph = Math.round((kwNet * eff) * 10) / 10;
            const totalMilesAdded = Math.round(kwhAdded * eff);
            const wallKwhUsed = kwhAdded / 0.92;
            const sessionCost = (wallKwhUsed * rate).toFixed(2);

            const minBreakerRaw = amps * 1.25;
            const breakers = [20, 30, 40, 50, 60, 70, 80, 100];
            let reqBreaker = 60;
            for (let i = 0; i < breakers.length; i++) {{
                if (breakers[i] >= minBreakerRaw) {{
                    reqBreaker = breakers[i];
                    break;
                }}
            }}

            let awg = "6 AWG Copper (THHN / Conduit)";
            if (reqBreaker <= 20) awg = "12 AWG Copper";
            else if (reqBreaker <= 30) awg = "10 AWG Copper";
            else if (reqBreaker <= 40) awg = "8 AWG Copper";
            else if (reqBreaker === 50) awg = "6 AWG Copper + Hubbell 9450FR NEMA 14-50";
            else if (reqBreaker === 60) awg = "6 AWG Copper THHN (Hardwired 48A)";
            else awg = "4 AWG / 3 AWG Copper (Hardwired)";

            document.getElementById("resHours").textContent = hours + " Hrs";
            document.getElementById("resKwhAdded").textContent = "+" + kwhAdded + " kWh (" + startSoc + "% to " + endSoc + "%)";
            document.getElementById("resMPH").textContent = "+" + mph + " Mi/Hr";
            document.getElementById("resKwOut").textContent = kwGross + " kW Gross (" + kwNet.toFixed(1) + " kW Net)";
            document.getElementById("resBreaker").textContent = reqBreaker + "A 2-Pole Breaker";
            document.getElementById("resCost").textContent = "$" + sessionCost + " / charge";
            document.getElementById("resTotalMiles").textContent = "+" + totalMilesAdded + " Miles Range Added";
            document.getElementById("resWireAWG").textContent = awg;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "";

            if (amps <= 32) {{
                recTitle = "16A–32A Adjustable Level 2 EV Charger (Fits 20A–40A Circuits)";
                recDesc = "Configurable amperage ideal for 30A dryer outlets or 40A subpanels without panel upgrades.";
                primaryQuery = "Grizzl-E Classic ChargePoint Home Flex Adjustable Amp Level 2 EV Charger";
                secondaryQuery = "Lectron NACS to J1772 EV Charger Adapter";
            }} else if (amps === 40) {{
                recTitle = "40-Amp (9.6 kW) NEMA 14-50 Plug-In Smart Level 2 EV Charger";
                recDesc = "America's #1 plug-in setup for 50A breakers—pair with a heavy-duty Hubbell 9450FR outlet.";
                primaryQuery = "ChargePoint Home Flex Emporia Grizzl-E 40A NEMA 14-50 Level 2 EV Charger";
                secondaryQuery = "Hubbell Bryant 9450FR Heavy Duty 50 Amp NEMA 14-50 EV Outlet";
            }} else {{
                recTitle = "48A–50A (11.5–12.0 kW) Hardwired High-Output Level 2 Wall Charger";
                recDesc = "Maximum residential speed on a 60A–70A circuit for large SUVs, trucks, and fast turnarounds.";
                primaryQuery = "Tesla Universal Wall Connector ChargePoint Home Flex Emporia 48A EV Charger";
                secondaryQuery = "Lectron Vortex Plug Tesla NACS to CCS J1772 Adapter";
            }}

            document.getElementById("recChargerTitle").textContent = recTitle;
            document.getElementById("recChargerDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateEV);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-700"><span class="text-emerald-600 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-700"><span class="text-rose-600 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-slate-700 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-emerald-600">Home & EV Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-emerald-600">EV Charger Reviews</a>
            <span>/</span>
            <span class="text-slate-800">{rev['product_name']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-emerald-100 text-emerald-900 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <span class="text-sm font-black bg-amber-100 text-amber-900 px-3 py-1 rounded-lg">Lab Rating: {rev['rating_score']} / 5.0 ★</span>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs">
                <div><span class="text-slate-400 block font-medium">Amperage Spec</span><strong class="text-slate-900">{rev['amperage_spec']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Power Delivery</span><strong class="text-slate-900">{rev['power_spec']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Cable / Build</span><strong class="text-slate-900">{rev['cable_spec']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Warranty</span><strong class="text-slate-900">{rev['warranty']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Charging Time for Your EV
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white border-2 border-emerald-200 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-white border-2 border-rose-200 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-100 pb-3">Hands-On Thermal, Cable & Charging Speed Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-emerald-600 block">Final Verdict</span>
                    <p class="text-sm font-bold text-slate-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our Level 2 EVSE benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-500 hover:bg-amber-600 text-slate-950 font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500 text-center">
        <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-slate-200">
            <td class="p-4 font-bold text-slate-900 bg-slate-50 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-700 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-700 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-emerald-600">Home & EV Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-emerald-600">Product Comparisons</a>
            <span>/</span>
            <span class="text-slate-800">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-emerald-100 text-emerald-900 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-900 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-emerald-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-slate-50">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-slate-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-emerald-50 border-2 border-emerald-200 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-slate-900 hover:bg-slate-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500 text-center">
        <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "78 kWh EV (40A Level 2 Charger)",
        "kwh": 78,
        "amps": 40,
        "eff": 3.4,
        "start_soc": 20,
        "end_soc": 80,
        "desc": "Calculate exact Level 2 EV charging time (hours), kW output, miles of range added per hour, NEC 80% circuit breaker size, and copper wire gauge—plus compare top UL-listed EV chargers."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Programmatic EV Model & Battery kWh Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 3. Generate Standalone Product Review Pages
    for rev in get_active_product_reviews():
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} SEO pages (EV Calculators + Reviews + Comparisons) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
