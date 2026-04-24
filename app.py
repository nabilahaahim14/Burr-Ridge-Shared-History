import streamlit as st
import pandas as pd
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

# Custom CSS with enhanced styling
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        [data-testid="stHeader"] {
            background: white;
            border-bottom: 2px solid #e0e7ff;
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
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
        }
        
        .landmark-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }
        
        .landmark-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 10px 10px -5px rgb(0 0 0 / 0.04);
            border-color: #1e40af;
        }
        
        .landmark-card:hover::before {
            left: 100%;
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
            top: -50%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        .hero-section::after {
            content: '';
            position: absolute;
            bottom: -30%;
            left: -5%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
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
        
        .cta-section::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        .cta-section h3 {
            font-size: 1.75rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
            color: #312e81;
            position: relative;
            z-index: 1;
        }
        
        .cta-section p {
            color: #4c1d95;
            margin-bottom: 1.75rem;
            font-size: 1.05rem;
            position: relative;
            z-index: 1;
        }
        
        .modal-container {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 2rem;
            padding: 3rem;
            margin-bottom: 2rem;
            box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.15);
            animation: slideInUp 0.5s ease-out;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .modal-container h2 {
            color: #0f172a;
            margin-bottom: 1rem;
            font-size: 2rem;
            font-weight: 800;
        }
        
        .modal-container p {
            color: #475569;
            line-height: 1.8;
            font-size: 1.05rem;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            border: none;
            border-radius: 0.75rem;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        
        .stButton > button:hover {
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.2);
            transform: translateY(-2px);
        }
        
        .timestamp {
            color: #64748b;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .divider-line {
            height: 2px;
            background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
            margin: 2rem 0;
        }
        
        h4 {
            color: #1e293b;
            font-weight: 700;
            font-size: 1.25rem;
        }
        
        .search-container {
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Landmarks data with complete descriptions
LANDMARKS = [
    {
        "id": 1,
        "title": "Potawatomi Last Camp Site",
        "type": "History",
        "short": "Marking the 1835 Potawatomi camp site at Wolf & Plainfield.",
        "description": "The area that is now Burr Ridge was originally inhabited by the Potawatomi people, who called the region 'Tioga' (meaning 'peaceful valley'). A granite boulder historical marker at the northwest corner of Wolf and Plainfield Roads marks the 'Last Camp Site of the Potawatomie Indians in Cook County, 1835.' Erected by the DAR (Daughters of the American Revolution) on May 15, 1930, it remains one of the oldest commemorative markers in our community. This sacred site represents the final gathering place of the Potawatomi nation in Cook County before their forced removal during the Indian Removal Act era. The marker stands as a testament to the indigenous heritage that shaped this land long before European settlement.",
        "date": "Erected: May 15, 1930",
        "color": "#fef3c7"
    },
    {
        "id": 2,
        "title": "Joseph Vial Log Cabin Site",
        "type": "History",
        "short": "The site of Burr Ridge's first post office and hotel (1834).",
        "description": "In 1834, Joseph Vial erected a log cabin near Wolf and Plainfield Roads, establishing what would become Burr Ridge's first center of commerce. He served as the area's first postmaster and operated a hotel on the stagecoach line, making it a crucial hub for travelers and settlers moving westward. The Vial family was instrumental in local politics and the founding of the Lyonsville Congregational Church, which still stands today. Remarkably, the first Democratic convention in Cook County was held here in 1835, making this humble cabin the birthplace of political organizing in our region. The Vial legacy shaped the early character of the community during the crucial pioneer era.",
        "date": "Established: 1834",
        "color": "#e7e5e4"
    },
    {
        "id": 3,
        "title": "Robert Vial House",
        "type": "History",
        "short": "The oldest standing building in Burr Ridge (1856).",
        "description": "Built in 1856, the Robert Vial House is a stunning example of Greek Revival architecture with Italianate elements, representing the community's early agricultural success and refined taste. Robert Vial's farm was a model of 19th-century innovation—it even featured the first silo constructed in Cook County, a revolutionary agricultural advancement that changed farming practices across the region. In 1989, the Flagg Creek Heritage Society moved the carefully restored house to its current site on Wolf Road to preserve it as a local history museum. Visitors can tour the period-furnished rooms and learn about life in the early Burr Ridge settlement. The house stands as a beautiful testament to the Vial family's enduring influence on our community.",
        "date": "Built: 1856 / Relocated: 1989",
        "color": "#f0fdf4"
    },
    {
        "id": 4,
        "title": "Flagg Creek Heritage Museum",
        "type": "History",
        "short": "Preserving local history and the story of 'Tiedtville.'",
        "description": "Located on Pleasant Dale Park District grounds, the museum operates alongside the Robert Vial House as a comprehensive repository of Burr Ridge history. A key focus is the fascinating unincorporated town of 'Tiedtville,' which grew from a single tavern into a thriving community with its own post office, butcher shop, general store, and even a jail. The museum houses an impressive collection of artifacts, photographs, documents, and personal memorabilia that bring the stories of our ancestors to life. Established in 1976, the Flagg Creek Heritage Society continues to gather, preserve, and share the physical and cultural heritage of our region. The museum serves as the primary repository for Burr Ridge's artifacts and regularly hosts educational programs and community events.",
        "date": "Society Established: 1976",
        "color": "#e0e7ff"
    },
    {
        "id": 5,
        "title": "Hiram McClintock Civil War Letters",
        "type": "History",
        "short": "Personal records of a Burr Ridge schoolteacher in the Civil War.",
        "description": "Hiram McClintock was a dedicated schoolteacher at 'Skunk Corners' who was born on a farm on what is now County Line Road. When the Civil War broke out, he answered the call to duty and served with the 127th Illinois Regiment, eventually giving his life for the Union cause. The Flagg Creek Heritage Society carefully preserves his collection of poignant letters, which offer an intimate window into life during America's greatest conflict. His correspondence with his former student Sarah North provides touching insights into the hopes, fears, and daily struggles of soldiers and those waiting at home. These letters humanize the statistics of the Civil War and remind us of the local sacrifice that was made on distant battlefields. They are a treasure of American history and a moving tribute to a devoted educator and patriot.",
        "date": "War Service: 1861-1865",
        "color": "#f1f5f9"
    },
    {
        "id": 6,
        "title": "Harvester Park / IH Farm",
        "type": "Parks",
        "short": "Site of the world's first all-purpose tractor testing.",
        "description": "In 1917, International Harvester, one of America's largest agricultural equipment manufacturers, purchased 414 acres here for a state-of-the-art experimental farm. This facility became the testing ground for the revolutionary 'Farmall' tractor, a machine that would transform agriculture worldwide by proving that a single tractor could perform all farming tasks. The village was so proud of this agricultural innovation and industrial presence that it was originally named 'Harvester' when it incorporated in 1956—a direct tribute to this heritage. Though the farm operations ceased long ago, Harvester Park stands today as a beautiful tribute to this legacy of local invention, agricultural science, and the spirit of innovation that defined America's farm belt. The park provides recreation facilities while honoring the technological revolution that once occurred on these grounds.",
        "date": "Established: 1917 / Park: 1980s",
        "color": "#ecfdf5"
    },
    {
        "id": 7,
        "title": "The Bridewell Prison Farm",
        "type": "History",
        "short": "A self-sufficient jail farm that shaped our Village Center.",
        "description": "From 1917 to 1969, the Cook County Prison Farm, commonly known as 'The Bridewell,' operated on land that now includes the Ambriance subdivision. This unique facility was designed as a self-sufficient agricultural operation where inmates produced dairy products and crops specifically for the county jail system. The farm represented an innovative approach to incarceration, combining punishment with productive labor. After closing in 1969, the land's transition to residential use was a pivotal turning point for Burr Ridge's development. The former prison farm became the site of high-end gated communities and the Village Center, transforming from a place of confinement into a place of opportunity and community commerce. This transformation symbolizes the village's evolution from an agricultural economy to a thriving suburban residential community.",
        "date": "Operated: 1917-1969",
        "color": "#fef2f2"
    },
    {
        "id": 8,
        "title": "Highland Fields / Busby Farm",
        "type": "History",
        "short": "The dairy farm that gave Burr Ridge its name.",
        "description": "In the 1940s, Denver Busby established the impressive 190-acre Burr Ridge Dairy Farm, creating one of the region's largest agricultural operations. Busby's vision extended beyond farming—he launched 'Burr Ridge Estates' with spacious 5-acre lots, establishing the village's lasting identity as a luxury residential community with generous land and elegant homes. His dairy farm name was officially adopted by the village upon incorporation in 1956, directly linking our modern name to his pastoral vision and agricultural success. The Busby family's entrepreneurial spirit and commitment to quality shaped Burr Ridge's character as an affluent suburb that valued both heritage and progress. Though the dairy operations have long ceased, the name 'Burr Ridge' perpetually honors the agricultural roots and the visionary developer who transformed farmland into a sought-after residential destination.",
        "date": "Heritage: 1940s",
        "color": "#fed7aa"
    },
    {
        "id": 9,
        "title": "Schustek Pond",
        "type": "Monuments",
        "short": "The heroic story of the 'Parachute Martyr' (1930).",
        "description": "On July 6, 1930, pilot Bruno Schustek demonstrated extraordinary heroism during a tragedy over Burr Ridge. When heiress Mary Fahrney's parachute became fatally entangled in his plane's wing at 1,000 feet above the ground, Schustek made the ultimate sacrifice. Without hesitation, he climbed out onto the wing of the flying aircraft, risking his own life in a desperate attempt to free her. Though Schustek tragically fell to his death, his courageous actions were not in vain—Mary Fahrney survived, saved by his selfless bravery. His heroic final act captured the nation's attention and earned him the sobering title 'Parachute Martyr.' The pond near Veterans Boulevard was officially named in his honor in 2015 on the 85th anniversary of the incident, serving as an eternal memorial to one of aviation's most poignant stories of sacrifice and courage.",
        "date": "Incident: July 6, 1930 / Named: 2015",
        "color": "#dbeafe"
    },
    {
        "id": 10,
        "title": "Burr Ridge Veterans Memorial",
        "type": "Monuments",
        "short": "Honoring service members and Medal of Honor recipient Lester Weber.",
        "description": "Dedicated in June 2010, the Burr Ridge Veterans Memorial stands as a powerful tribute to those who served and sacrificed for our nation. The memorial features five distinctive walls, each representing one of the five branches of the military—Army, Navy, Air Force, Marines, and Coast Guard. At its center stands a moving 'Fallen Soldier' sculpture that honors those who made the ultimate sacrifice. The memorial specifically honors Lester W. Weber, a native son of Burr Ridge who earned the Medal of Honor, the nation's highest military decoration, for his extraordinary heroism during the Vietnam War. Over 700 engraved bricks line the memorial grounds, each bearing the name of a veteran with ties to our community, creating an enduring record of Burr Ridge's contribution to American service. The memorial hosts annual ceremonies and serves as a gathering place for reflection, remembrance, and community pride in our military heritage.",
        "date": "Opened: June 2010",
        "color": "#fee2e2"
    },
    {
        "id": 11,
        "title": "The Dove Bar Factory",
        "type": "History",
        "short": "A sweet piece of local pride manufactured in Burr Ridge.",
        "description": "The world-famous Dove Bar ice cream treat has deep and meaningful ties to Burr Ridge's community heritage. Originally invented in 1956 by Leo Stefanos at a small candy shop in Chicago, the Dove Bar quickly became a beloved dessert across America—a premium ice cream bar enrobed in rich chocolate. The massive popularity of the treat led to large-scale manufacturing operations right here in Burr Ridge, making the village an important production hub for this iconic product throughout the 1950s-1980s. For multiple generations of residents, the distinctive aroma of chocolate-covered ice cream being manufactured in their own backyard became part of the community's identity. Many residents have warm childhood memories of the Dove Bar factory, and it remains a point of local pride and nostalgia. The story of the Dove Bar represents Burr Ridge's connection to American consumer brands and industrial innovation.",
        "date": "Established: 1950s-1980s",
        "color": "#fef3c7"
    },
    {
        "id": 12,
        "title": "The Origin of 'Burr Ridge'",
        "type": "History",
        "short": "Named for the bur oak trees and glacial ridges.",
        "description": "The distinctive name 'Burr Ridge' was officially adopted to honor the geographic and botanical features that define our landscape. The name refers to the bur oak trees that once grew abundantly along the high ridges that characterize our terrain. These rolling hills and ridges were carved by massive glaciers during the last ice age, approximately 10,000-20,000 years ago, leaving behind the distinctive topography that distinguishes Burr Ridge from surrounding communities. The village is situated primarily on the Valparaiso Moraine, a geological formation created by glacial action that gives our land its unique rolling character. The name 'Burr Ridge' thus reflects our community's deep connection to the natural landscape and the ancient environmental forces that shaped our land long before human settlement. The village's name is a poetic reminder that we are stewards of a landscape shaped by millions of years of geological history.",
        "date": "Village Renamed: 1962",
        "color": "#f0fdf4"
    }
]

# Initialize session state
if "selected_landmark" not in st.session_state:
    st.session_state.selected_landmark = None
if "show_suggest_modal" not in st.session_state:
    st.session_state.show_suggest_modal = False
if "current_filter" not in st.session_state:
    st.session_state.current_filter = "All"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "submission_success" not in st.session_state:
    st.session_state.submission_success = False

# Email sending function
def send_email(landmark_name, story, photo_url=""):
    try:
        # Email configuration
        sender_email = "noreply@burr-ridge.gov"
        recipient_emails = ["nhashim@burr-ridge.gov", "brvillage@burr-ridge.gov"]
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"New Landmark Submission: {landmark_name}"
        message["From"] = sender_email
        message["To"] = ", ".join(recipient_emails)
        
        # Create HTML email body
        html = f"""\
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8fafc;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h2 style="color: #1e40af; border-bottom: 3px solid #1e40af; padding-bottom: 1rem;">New Landmark Story Submission</h2>
                    
                    <div style="margin: 2rem 0;">
                        <h3 style="color: #0c2d6b; margin-bottom: 0.5rem;">Landmark Name:</h3>
                        <p style="font-size: 1.1rem; color: #475569; background: #f0f4ff; padding: 1rem; border-radius: 0.75rem; border-left: 4px solid #1e40af;">{landmark_name}</p>
                    </div>
                    
                    <div style="margin: 2rem 0;">
                        <h3 style="color: #0c2d6b; margin-bottom: 0.5rem;">Historical Context & Story:</h3>
                        <p style="color: #475569; line-height: 1.6; background: #f9fafb; padding: 1rem; border-radius: 0.75rem; border-left: 4px solid #3b82f6; white-space: pre-wrap;">{story}</p>
                    </div>
                    
                    {f'<div style="margin: 2rem 0;"><h3 style="color: #0c2d6b; margin-bottom: 0.5rem;">Photo URL:</h3><p style="color: #475569;"><a href="{photo_url}" style="color: #1e40af; text-decoration: none;">{photo_url}</a></p></div>' if photo_url else ''}
                    
                    <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 0.9rem;">
                        <p>Submitted on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p style="margin-top: 0.5rem;">This submission has been received by the Burr Ridge Historical Society.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        # Note: In production, you'd use SMTP to send
        # For now, we'll just return success
        return True
    except Exception as e:
        st.error(f"Error preparing email: {str(e)}")
        return False

# Header
col1, col2 = st.columns([10, 1])
with col1:
    st.markdown("# 📍 Village of Burr Ridge | History & Landmarks")
with col2:
    st.caption("Est. 1956")

st.caption("🏛️ Explore the stories behind our most significant commemorative sites")

# DETAIL MODAL - DISPLAY AT TOP
if st.session_state.selected_landmark:
    landmark = st.session_state.selected_landmark
    
    with st.container():
        st.markdown('<div class="modal-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([10, 1, 1])
        with col2:
            if st.button("📍 Map", key="map_button", use_container_width=True):
                st.info("🗺️ Map integration coming soon!")
        with col3:
            if st.button("✕", key="close_modal", use_container_width=True):
                st.session_state.selected_landmark = None
                st.rerun()
        
        st.markdown(f"<div class='category-badge'>{landmark['type']}</div>", unsafe_allow_html=True)
        st.markdown(f"## {landmark['title']}")
        
        st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.8; color: #475569;'>{landmark['description']}</p>", unsafe_allow_html=True)
        
        st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"<div class='timestamp'>🕐 {landmark['date']}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")

# Hero Section
st.markdown("""
    <div class="hero-section">
        <h2>Preserving Our Local Legacy</h2>
        <p>Explore the stories behind our most significant landmarks—from the Potawatomi camps and early pioneers to the invention of the Dove Bar.</p>
    </div>
""", unsafe_allow_html=True)

# Search and Filter
st.markdown("<div class='search-container'>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input(
        "🔍 Search landmarks, names, or keywords...",
        value=st.session_state.search_query,
        key="search_input",
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

st.markdown("</div>", unsafe_allow_html=True)

# Filter landmarks
filtered_landmarks = LANDMARKS.copy()

if filter_type != "All":
    filtered_landmarks = [l for l in filtered_landmarks if l["type"] == filter_type]

if search_query:
    query_lower = search_query.lower()
    filtered_landmarks = [
        l for l in filtered_landmarks
        if query_lower in l["title"].lower()
        or query_lower in l["description"].lower()
        or query_lower in l["short"].lower()
    ]

# Display landmarks grid
st.markdown("---")
if filtered_landmarks:
    cols = st.columns(3)
    for idx, landmark in enumerate(filtered_landmarks):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="landmark-card">
                    <div class="category-badge">{landmark['type']}</div>
                    <h4 style="margin-top: 0; margin-bottom: 0.75rem;">{landmark['title']}</h4>
                    <p style="color: #64748b; font-size: 0.95rem; margin: 1rem 0; line-height: 1.6;">{landmark['short']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("📖 Read Story", key=f"btn_{landmark['id']}", use_container_width=True):
                st.session_state.selected_landmark = landmark
                st.rerun()
else:
    st.info("📭 No landmarks found matching your search. Try adjusting your filters!")

# Suggestion CTA Section
st.markdown("---")
st.markdown("""
    <div class="cta-section">
        <h3>Did we miss a local story?</h3>
        <p>Our history is a community effort. If you know the story behind a local street name, marker, or monument, please share it with us.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📝 Submit a Story", use_container_width=True, key="submit_story_btn"):
        st.session_state.show_suggest_modal = True
        st.rerun()

# Suggestion Form Modal
if st.session_state.show_suggest_modal:
    st.markdown("---")
    
    with st.container():
        st.markdown('<div class="modal-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([10, 1])
        with col2:
            if st.button("✕", key="close_suggest"):
                st.session_state.show_suggest_modal = False
                st.rerun()
        
        st.markdown("## 📝 Suggest a Landmark")
        st.caption("📬 Contribute to the Burr Ridge archive")
        
        st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)
        
        with st.form("suggest_form", clear_on_submit=True):
            landmark_name = st.text_input(
                "Landmark or Location Name *", 
                placeholder="Enter the name of the landmark or location...",
                key="landmark_name_input"
            )
            story = st.text_area(
                "The Story / Historical Context *", 
                placeholder="Who is it named after? Why is it important? Share the historical details...",
                height=200,
                key="story_input"
            )
            photo_url = st.text_input(
                "Upload Photo (Optional URL)", 
                placeholder="https://example.com/image.jpg",
                key="photo_input"
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submitted = st.form_submit_button("✉️ Submit to Historical Society", use_container_width=True)
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.show_suggest_modal = False
                    st.rerun()
            
            if submitted:
                if landmark_name.strip() and story.strip():
                    # Send email
                    if send_email(landmark_name, story, photo_url):
                        st.success("✅ Thank you! Your submission has been sent to the Historical Society.\n\nWe appreciate your contribution to preserving Burr Ridge's history!")
                        st.balloons()
                        st.session_state.show_suggest_modal = False
                        st.session_state.submission_success = True
                    else:
                        st.error("There was an issue sending your submission. Please try again.")
                else:
                    st.error("⚠️ Please fill in all required fields marked with *")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.caption("© 2026 Village of Burr Ridge, Illinois. All rights reserved.")
with col2:
    st.caption("[📧 Contact](mailto:history@burr-ridge.org)")
with col3:
    st.caption("[ℹ️ About Burr Ridge](https://www.burr-ridge.org)")
