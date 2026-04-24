import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Commemorative Landmarks of Burr Ridge",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }

        [data-testid="stHeader"] {
            background: white;
            border-bottom: 2px solid #e0e7ff;
        }

        .landmark-card {
            border: 1px solid #e2e8f0;
            border-radius: 1.5rem;
            padding: 1.75rem;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            height: 100%;
        }

        .landmark-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 10px 10px -5px rgb(0 0 0 / 0.04);
            border-color: #1e40af;
        }

        .hero-section {
            background: linear-gradient(135deg, #0c2d6b 0%, #1e40af 50%, #3b82f6 100%);
            color: white;
            padding: 4rem 2rem;
            border-radius: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
            position: relative;
            overflow: hidden;
        }

        .hero-section::before {
            content: '';
            position: absolute;
            top: -50%; right: -10%;
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            border-radius: 50%;
        }

        .hero-section h2 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            position: relative;
            z-index: 1;
            letter-spacing: -1px;
        }

        .hero-section p {
            font-size: 1.2rem;
            color: #bfdbfe;
            margin-bottom: 2rem;
            position: relative;
            z-index: 1;
            line-height: 1.8;
        }

        .category-badge {
            display: inline-block;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            color: #0c4a6e;
            padding: 0.35rem 0.95rem;
            border-radius: 0.75rem;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            margin-bottom: 0.75rem;
            border: 1px solid #bae6fd;
            text-transform: uppercase;
        }

        .cta-section {
            background: linear-gradient(135deg, #f0f4ff 0%, #ede9fe 100%);
            padding: 3rem 2rem;
            border-radius: 2rem;
            text-align: center;
            margin-top: 4rem;
            border: 2px solid #c7d2fe;
            position: relative;
            overflow: hidden;
        }

        .cta-section h3 {
            font-size: 1.75rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
            color: #312e81;
        }

        .cta-section p {
            color: #4c1d95;
            margin-bottom: 1.75rem;
            font-size: 1.05rem;
        }

        /* Dialog / Modal overrides */
        [data-testid="stDialog"] > div {
            border-radius: 1.5rem !important;
            overflow: hidden;
            max-width: 680px !important;
        }

        .dialog-header {
            background: linear-gradient(135deg, #0c2d6b 0%, #1e40af 60%, #3b82f6 100%);
            color: white;
            padding: 2rem 2rem 1.5rem;
            border-radius: 1.2rem 1.2rem 0 0;
            margin: -1rem -1rem 1.5rem -1rem;
        }

        .dialog-category {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 0.5rem;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-bottom: 0.6rem;
            border: 1px solid rgba(255,255,255,0.3);
            text-transform: uppercase;
        }

        .dialog-title {
            font-size: 1.7rem;
            font-weight: 800;
            color: white;
            margin: 0;
            line-height: 1.2;
        }

        .dialog-description {
            color: #475569;
            line-height: 1.85;
            font-size: 1.0rem;
            margin: 0 0 1.5rem 0;
        }

        .location-card {
            background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%);
            border: 1px solid #c7d2fe;
            border-radius: 1rem;
            padding: 1.25rem 1.5rem;
            margin-top: 1.5rem;
        }

        .location-card-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: #3730a3;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
        }

        .location-card-address {
            font-size: 1rem;
            color: #1e293b;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .location-card-coords {
            font-size: 0.82rem;
            color: #64748b;
            font-family: monospace;
        }

        .date-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            color: #475569;
            padding: 0.45rem 0.9rem;
            border-radius: 0.65rem;
            font-size: 0.85rem;
            margin-top: 1rem;
        }

        .divider-line {
            height: 2px;
            background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
            margin: 1.5rem 0;
        }

        h4 { color: #1e293b; font-weight: 700; font-size: 1.2rem; }

        .stButton > button {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            border: none;
            border-radius: 0.75rem;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }

        .stButton > button:hover {
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.2);
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

# ─── Landmarks Data ───────────────────────────────────────────────────────────
LANDMARKS = [
    {
        "id": 1,
        "title": "Potawatomi Last Camp Site",
        "type": "History",
        "short": "Marking the 1835 Potawatomi camp site at Wolf & Plainfield.",
        "description": "The area that is now Burr Ridge was originally inhabited by the Potawatomi people, who called the region 'Tioga' (meaning 'peaceful valley'). A granite boulder historical marker at the northwest corner of Wolf and Plainfield Roads marks the 'Last Camp Site of the Potawatomie Indians in Cook County, 1835.' Erected by the DAR (Daughters of the American Revolution) on May 15, 1930, it remains one of the oldest commemorative markers in our community. This sacred site represents the final gathering place of the Potawatomi nation in Cook County before their forced removal during the Indian Removal Act era.",
        "date": "Erected: May 15, 1930",
        "location_text": "NW corner of Wolf Road & Plainfield Road\nBurr Ridge, IL 60527",
        "maps_url": "https://www.google.com/maps/search/Wolf+Road+%26+Plainfield+Road,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 2,
        "title": "Joseph Vial Log Cabin Site",
        "type": "History",
        "short": "The site of Burr Ridge's first post office and hotel (1834).",
        "description": "In 1834, Joseph Vial erected a log cabin near Wolf and Plainfield Roads, establishing what would become Burr Ridge's first center of commerce. He served as the area's first postmaster and operated a hotel on the stagecoach line, making it a crucial hub for travelers and settlers moving westward. The Vial family was instrumental in local politics and the founding of the Lyonsville Congregational Church. Remarkably, the first Democratic convention in Cook County was held here in 1835, making this humble cabin the birthplace of political organizing in our region.",
        "date": "Established: 1834",
        "location_text": "Near Wolf Road & Plainfield Road\nBurr Ridge, IL 60527\n(Historical site — no marker currently standing)",
        "maps_url": "https://www.google.com/maps/search/Wolf+Road+%26+Plainfield+Road,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 3,
        "title": "Robert Vial House",
        "type": "History",
        "short": "The oldest standing building in Burr Ridge (1856).",
        "description": "Built in 1856, the Robert Vial House is a stunning example of Greek Revival architecture with Italianate elements. Robert Vial's farm was a model of 19th-century innovation — it even featured the first silo constructed in Cook County, a revolutionary agricultural advancement. In 1989, the Flagg Creek Heritage Society carefully moved and restored the house to its current site on Wolf Road as a local history museum. Visitors can tour the period-furnished rooms and learn about life in the early Burr Ridge settlement.",
        "date": "Built: 1856 / Relocated: 1989",
        "location_text": "7425 S. Wolf Road\nBurr Ridge, IL 60527\n(Pleasant Dale Park District grounds)",
        "maps_url": "https://www.google.com/maps/search/7425+S+Wolf+Road,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 4,
        "title": "Flagg Creek Heritage Museum",
        "type": "History",
        "short": "Preserving local history and the story of 'Tiedtville.'",
        "description": "Located on Pleasant Dale Park District grounds alongside the Robert Vial House, this museum serves as the primary repository for Burr Ridge's artifacts and heritage. A key exhibit explores the fascinating unincorporated town of 'Tiedtville,' which grew from a single tavern into a community with its own post office, butcher shop, general store, bowling alley, and even a jail. Established in 1976, the Flagg Creek Heritage Society continues to gather, preserve, and share the cultural history of the region through exhibits, lectures, and community programs.",
        "date": "Society Established: 1976",
        "location_text": "7425 S. Wolf Road\nBurr Ridge, IL 60527\nOpen: 1st Sunday (Apr–Oct), 2–4 PM · Most Mondays 10 AM–1 PM",
        "maps_url": "https://www.google.com/maps/search/7425+S+Wolf+Road,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 5,
        "title": "Hiram McClintock Civil War Letters",
        "type": "History",
        "short": "Personal records of a Burr Ridge schoolteacher in the Civil War.",
        "description": "Hiram McClintock was a dedicated schoolteacher at 'Skunk Corners' (Joliet Road & East Avenue) born on a farm on what is now County Line Road. When the Civil War broke out, he served with the 127th Illinois Regiment and gave his life for the Union cause. The Flagg Creek Heritage Society preserves his collection of letters, offering an intimate window into life during America's greatest conflict. His correspondence with former student Sarah North provides touching insight into the hopes and fears of soldiers and those waiting at home — a treasure of American local history.",
        "date": "War Service: 1861–1865",
        "location_text": "Flagg Creek Heritage Museum\n7425 S. Wolf Road, Burr Ridge, IL 60527\n(Letters housed in the museum collection)",
        "maps_url": "https://www.google.com/maps/search/7425+S+Wolf+Road,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 6,
        "title": "Harvester Park / IH Experimental Farm",
        "type": "Parks",
        "short": "Site of the world's first all-purpose tractor testing.",
        "description": "In 1917, International Harvester purchased 414 acres here for a state-of-the-art experimental farm. This facility became the testing ground for the revolutionary 'Farmall' tractor — a machine that transformed agriculture worldwide by proving a single tractor could perform all farming tasks. The village was so proud of this legacy that it named itself 'Harvester' upon incorporation in 1956. Harvester Park stands today as a tribute to this spirit of innovation, providing recreation facilities while honoring the agricultural science revolution that once occurred on these very grounds.",
        "date": "Farm Established: 1917 / Park Acquired: 1990",
        "location_text": "15W400 Harvester Drive\nBurr Ridge, IL 60527\n📞 (630) 920-1969",
        "maps_url": "https://www.google.com/maps/search/15W400+Harvester+Drive,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 7,
        "title": "The Bridewell Prison Farm",
        "type": "History",
        "short": "A self-sufficient jail farm that shaped our Village Center.",
        "description": "From 1917 to 1969, the Cook County Prison Farm — known as 'The Bridewell' — operated on land that now includes parts of the Ambriance subdivision and Village Center. This unique facility had inmates produce dairy products and crops specifically for the county jail system. After its closure in 1969, Mayor Richard J. Daley proposed building subsidized housing here, but DuPage County blocked the plan. The land was eventually transformed into high-end gated communities and commercial developments — a remarkable shift from a place of confinement to one of the most sought-after addresses in Burr Ridge.",
        "date": "Operated: 1917–1969",
        "location_text": "Ambriance Subdivision & Village Center area\nBurr Ridge, IL 60527\n(Site of former farm, now residential/commercial)",
        "maps_url": "https://www.google.com/maps/search/Ambriance+Burr+Ridge+IL+60527",
    },
    {
        "id": 8,
        "title": "Highland Fields / Busby Dairy Farm",
        "type": "History",
        "short": "The dairy farm that gave Burr Ridge its name.",
        "description": "In the 1940s, Denver Busby established a 190-acre dairy farm and launched 'Burr Ridge Estates' with spacious 5-acre lots — establishing the village's identity as a luxury residential community. His farm's name was officially adopted by the village in 1962, directly linking Burr Ridge's modern name to his pastoral vision. The Busby family's entrepreneurial spirit shaped the character of Burr Ridge as an affluent suburb that valued both heritage and progress. Though the dairy operations ceased long ago, the village name permanently honors the agricultural roots of this visionary developer.",
        "date": "Heritage: 1940s / Village Renamed: 1962",
        "location_text": "Highland Fields Subdivision\nBurr Ridge, IL 60527\n(Area of former Busby dairy farm, now residential)",
        "maps_url": "https://www.google.com/maps/search/Highland+Fields,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 9,
        "title": "Schustek Pond",
        "type": "Monuments",
        "short": "The heroic story of the 'Parachute Martyr' (1930).",
        "description": "On July 6, 1930, WWI flying ace Bruno Schustek demonstrated extraordinary heroism when heiress Mary Fahrney's parachute became fatally entangled in a plane's wing at 1,000 feet above the ground. Without hesitation, Schustek climbed out onto the wing of a flying aircraft to try to free her — and tragically fell to his death. Fahrney survived. His courageous sacrifice earned him the title 'Parachute Martyr' and captured national attention. The pond on Veterans Boulevard was officially named in his honor in April 2015, with a dedication plaque unveiled on July 6, 2015 — exactly 85 years after his death.",
        "date": "Incident: July 6, 1930 / Named: April 2015",
        "location_text": "Schustek Pond, Veterans Blvd.\nBurr Ridge, IL 60527\n(Plaque in parking lot of 7075 Veterans Blvd)",
        "maps_url": "https://www.google.com/maps/search/7075+Veterans+Blvd,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 10,
        "title": "Burr Ridge Veterans Memorial",
        "type": "Monuments",
        "short": "Honoring service members and Medal of Honor recipient Lester Weber.",
        "description": "Dedicated in June 2010, this memorial features five stone-clad walls representing each branch of the military, a bronze 'Fallen Soldier' sculpture at center, and a six-foot bronze eagle. Over 700 engraved bricks bear the names of veterans with ties to our community. The memorial specifically honors Lester W. Weber, a Burr Ridge native who earned the Medal of Honor for extraordinary heroism during the Vietnam War. It took a dedicated committee of local veterans nine years to raise the over $300,000 needed to build it — a testament to community commitment to honoring those who served.",
        "date": "Opened: June 2010",
        "location_text": "7660 County Line Road\nBurr Ridge, IL 60527\n(Adjacent to Burr Ridge Village Hall, at County Line Rd & 77th St)",
        "maps_url": "https://www.google.com/maps/search/7660+County+Line+Road,+Burr+Ridge,+IL+60527",
    },
    {
        "id": 11,
        "title": "The Dove Bar Factory",
        "type": "History",
        "short": "A sweet piece of local pride manufactured in Burr Ridge.",
        "description": "The world-famous Dove Bar ice cream treat has deep ties to Burr Ridge's community heritage. Originally invented in 1956 by Leo Stefanos at a small Chicago candy shop, the Dove Bar became a beloved American dessert — a premium ice cream bar enrobed in rich chocolate. Its massive popularity led to large-scale manufacturing operations right here in Burr Ridge, making the village an important production hub throughout the 1950s–1980s. For generations of residents, the aroma of the Dove Bar factory was a part of everyday community life, and it remains a cherished point of local nostalgia.",
        "date": "Established: 1950s–1980s",
        "location_text": "Former factory site, Burr Ridge, IL 60527\n(Site has since been redeveloped)",
        "maps_url": "https://www.google.com/maps/search/Burr+Ridge,+IL+60527",
    },
    {
        "id": 12,
        "title": "The Origin of 'Burr Ridge'",
        "type": "History",
        "short": "Named for the bur oak trees and glacial ridges.",
        "description": "The name 'Burr Ridge' honors the bur oak trees that once grew abundantly along the high ridges defining our landscape. These rolling hills were carved by glaciers during the last ice age, leaving behind the Valparaiso Moraine — the geological formation that gives Burr Ridge its distinctive rolling character. Originally incorporated as 'Harvester' in 1956, the village was officially renamed 'Burr Ridge' in 1962 when the International Harvester estates and the Busby Burr Ridge Estates merged. The name is a poetic reminder that we are stewards of a landscape shaped by thousands of years of natural history.",
        "date": "Village Renamed: 1962",
        "location_text": "Village of Burr Ridge\nCook & DuPage Counties, IL 60527\n(Valparaiso Moraine runs throughout the village)",
        "maps_url": "https://www.google.com/maps/search/Burr+Ridge,+IL+60527",
    },
]

# ─── Session State ────────────────────────────────────────────────────────────
if "show_suggest_modal" not in st.session_state:
    st.session_state.show_suggest_modal = False
if "current_filter" not in st.session_state:
    st.session_state.current_filter = "All"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# ─── Email Helper ─────────────────────────────────────────────────────────────
def send_email(landmark_name, story, photo_url=""):
    try:
        sender_email = "noreply@burr-ridge.gov"
        recipient_emails = ["nhashim@burr-ridge.gov", "brvillage@burr-ridge.gov"]
        message = MIMEMultipart("alternative")
        message["Subject"] = f"New Landmark Submission: {landmark_name}"
        message["From"] = sender_email
        message["To"] = ", ".join(recipient_emails)
        html = f"""
        <html><body style="font-family: Arial, sans-serif; color: #333; background:#f8fafc;">
          <div style="max-width:600px;margin:0 auto;background:white;padding:2rem;border-radius:1rem;">
            <h2 style="color:#1e40af;border-bottom:3px solid #1e40af;padding-bottom:1rem;">New Landmark Story Submission</h2>
            <h3 style="color:#0c2d6b;">Landmark Name:</h3>
            <p style="background:#f0f4ff;padding:1rem;border-radius:.75rem;border-left:4px solid #1e40af;">{landmark_name}</p>
            <h3 style="color:#0c2d6b;">Story:</h3>
            <p style="background:#f9fafb;padding:1rem;border-radius:.75rem;border-left:4px solid #3b82f6;white-space:pre-wrap;">{story}</p>
            {f'<h3 style="color:#0c2d6b;">Photo URL:</h3><p><a href="{photo_url}">{photo_url}</a></p>' if photo_url else ''}
            <p style="color:#64748b;font-size:.9rem;border-top:1px solid #e2e8f0;margin-top:2rem;padding-top:1rem;">
              Submitted: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
          </div>
        </body></html>"""
        message.attach(MIMEText(html, "html"))
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# ─── Landmark Detail Dialog ───────────────────────────────────────────────────
@st.dialog("Landmark Detail", width="large")
def show_landmark_dialog(landmark):
    # Header block
    st.markdown(f"""
        <div class="dialog-header">
            <div class="dialog-category">{landmark['type']}</div>
            <div class="dialog-title">{landmark['title']}</div>
        </div>
    """, unsafe_allow_html=True)

    # Story
    st.markdown(f"<p class='dialog-description'>{landmark['description']}</p>", unsafe_allow_html=True)

    # Date badge
    st.markdown(f"<div class='date-badge'>🕐 {landmark['date']}</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

    # Location card
    st.markdown(f"""
        <div class="location-card">
            <div class="location-card-title">📍 Location</div>
            <div class="location-card-address">{landmark['location_text'].replace(chr(10), '<br>')}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("🗺️ Open in Google Maps", landmark['maps_url'], use_container_width=True)

# ─── Suggest Story Dialog ─────────────────────────────────────────────────────
@st.dialog("Suggest a Landmark Story", width="large")
def show_suggest_dialog():
    st.markdown("#### 📝 Contribute to the Burr Ridge Archive")
    st.caption("Share a story about a local street name, marker, monument, or historical site.")
    st.markdown("<div class='divider-line'></div>", unsafe_allow_html=True)

    with st.form("suggest_form", clear_on_submit=True):
        landmark_name = st.text_input(
            "Landmark or Location Name *",
            placeholder="e.g. Shustek Pond, Old Elm Street Bridge..."
        )
        story = st.text_area(
            "The Story / Historical Context *",
            placeholder="Who is it named after? Why is it important? Share the historical details...",
            height=180
        )
        photo_url = st.text_input(
            "Photo URL (optional)",
            placeholder="https://example.com/image.jpg"
        )
        submitted = st.form_submit_button("✉️ Submit to Historical Society", use_container_width=True)

        if submitted:
            if landmark_name.strip() and story.strip():
                if send_email(landmark_name, story, photo_url):
                    st.success("✅ Thank you! Your submission has been received by the Historical Society.")
                    st.balloons()
            else:
                st.error("⚠️ Please fill in the required fields marked with *")

# ─── Page Header ──────────────────────────────────────────────────────────────
col1, col2 = st.columns([10, 1])
with col1:
    st.markdown("# 📍 Village of Burr Ridge | History & Landmarks")
with col2:
    st.caption("Est. 1956")
st.caption("🏛️ Explore the stories behind our most significant commemorative sites")

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
    <div class="hero-section">
        <h2>Preserving Our Local Legacy</h2>
        <p>Explore the stories behind our most significant landmarks — from the Potawatomi camps and early pioneers to the invention of the Dove Bar.</p>
    </div>
""", unsafe_allow_html=True)

# ─── Search & Filter ──────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input(
        "🔍 Search landmarks, names, or keywords...",
        value=st.session_state.search_query,
        placeholder="Type to search..."
    )
    st.session_state.search_query = search_query
with col2:
    filter_type = st.selectbox(
        "Filter by Category",
        ["All", "History", "Parks", "Monuments"],
        index=["All", "History", "Parks", "Monuments"].index(st.session_state.current_filter)
    )
    st.session_state.current_filter = filter_type

# ─── Filter Landmarks ─────────────────────────────────────────────────────────
filtered = LANDMARKS.copy()
if filter_type != "All":
    filtered = [l for l in filtered if l["type"] == filter_type]
if search_query:
    q = search_query.lower()
    filtered = [l for l in filtered if q in l["title"].lower() or q in l["description"].lower() or q in l["short"].lower()]

# ─── Landmark Grid ────────────────────────────────────────────────────────────
st.markdown("---")
if filtered:
    cols = st.columns(3)
    for idx, landmark in enumerate(filtered):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="landmark-card">
                    <div class="category-badge">{landmark['type']}</div>
                    <h4 style="margin: 0 0 0.6rem;">{landmark['title']}</h4>
                    <p style="color: #64748b; font-size: 0.93rem; line-height: 1.6; margin: 0 0 1rem;">{landmark['short']}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("📖 Read Story", key=f"btn_{landmark['id']}", use_container_width=True):
                show_landmark_dialog(landmark)
else:
    st.info("📭 No landmarks found matching your search. Try adjusting your filters!")

# ─── CTA Section ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
    <div class="cta-section">
        <h3>Did we miss a local story?</h3>
        <p>Our history is a community effort. If you know the story behind a local street name, marker, or monument, please share it with us.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📝 Submit a Story", use_container_width=True):
        show_suggest_dialog()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.caption("© 2026 Village of Burr Ridge, Illinois. All rights reserved.")
with col2:
    st.caption("[📧 Contact](mailto:history@burr-ridge.org)")
with col3:
    st.caption("[ℹ️ About Burr Ridge](https://www.burr-ridge.org)")
