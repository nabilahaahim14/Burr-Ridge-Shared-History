import streamlit as st
import pandas as pd
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
        [data-testid="stAppViewContainer"] {
            background-color: #f8fafc;
        }
        
        [data-testid="stHeader"] {
            background-color: white;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .landmark-card {
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            padding: 1.5rem;
            background-color: white;
            box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            transition: all 0.3s ease;
        }
        
        .landmark-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        }
        
        .hero-section {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
        }
        
        .hero-section h2 {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        
        .hero-section p {
            font-size: 1.1rem;
            color: #bfdbfe;
            margin-bottom: 1.5rem;
        }
        
        .category-badge {
            display: inline-block;
            background-color: #eff6ff;
            color: #1e40af;
            padding: 0.25rem 0.75rem;
            border-radius: 0.5rem;
            font-size: 0.75rem;
            font-weight: bold;
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
        }
        
        .icon-box {
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.75rem;
            width: 3.5rem;
            height: 3.5rem;
            margin-bottom: 1rem;
        }
        
        .cta-section {
            background-color: #f1f5f9;
            padding: 2rem;
            border-radius: 1.5rem;
            text-align: center;
            margin-top: 4rem;
        }
        
        .cta-section h3 {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .cta-section p {
            color: #475569;
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Landmarks data
LANDMARKS = [
    {
        "id": 1,
        "title": "Potawatomi Last Camp Site",
        "type": "History",
        "short": "Marking the 1835 Potawatomi camp site at Wolf & Plainfield.",
        "description": "The area that is now Burr Ridge was originally inhabited by the Potawatomi people, who called the region 'Tioga' (meaning 'peaceful valley'). A granite boulder historical marker at the northwest corner of Wolf and Plainfield Roads marks the 'Last Camp Site of the Potawatomie Indians in Cook County, 1835.' Erected by the DAR on May 15, 1930, it remains one of the oldest commemorative markers in our community.",
        "date": "Erected: May 15, 1930",
        "color": "#fef3c7"
    },
    {
        "id": 2,
        "title": "Joseph Vial Log Cabin Site",
        "type": "History",
        "short": "The site of Burr Ridge's first post office and hotel (1834).",
        "description": "In 1834, Joseph Vial erected a log cabin near Wolf and Plainfield Roads. He served as the area's first postmaster and operated a hotel on the stagecoach line. The Vial family was instrumental in local politics and the founding of the Lyonsville Congregational Church. Remarkably, the first Democratic convention in Cook County was held here in 1835.",
        "date": "Established: 1834",
        "color": "#e7e5e4"
    },
    {
        "id": 3,
        "title": "Robert Vial House",
        "type": "History",
        "short": "The oldest standing building in Burr Ridge (1856).",
        "description": "Built in 1856, the Robert Vial House is a Greek Revival farmhouse with Italianate elements. It represents the community's early agricultural success; Robert Vial's farm even featured the first silo constructed in Cook County. In 1989, the Flagg Creek Heritage Society moved the house to its current site on Wolf Road to restore it as a local history museum.",
        "date": "Built: 1856 / Relocated: 1989",
        "color": "#f0fdf4"
    },
    {
        "id": 4,
        "title": "Flagg Creek Heritage Museum",
        "type": "History",
        "short": "Preserving local history and the story of 'Tiedtville.'",
        "description": "Located on Pleasant Dale Park District grounds, the museum operates alongside the Robert Vial House. A key focus is the unincorporated town of 'Tiedtville,' which grew from a single tavern into a town with its own post office, butcher shop, and even a jail. The museum serves as the primary repository for Burr Ridge's physical artifacts.",
        "date": "Society Established: 1976",
        "color": "#e0e7ff"
    },
    {
        "id": 5,
        "title": "Hiram McClintock Civil War Letters",
        "type": "History",
        "short": "Personal records of a Burr Ridge schoolteacher in the Civil War.",
        "description": "Hiram McClintock was a schoolteacher at 'Skunk Corners' who was born on a farm on what is now County Line Road. He served in the 127th Illinois Regiment and lost his life in the Civil War. The Flagg Creek Heritage Society preserves his collection of letters, which offer a poignant look at life during the war, including correspondence with his student Sarah North.",
        "date": "War Service: 1861-1865",
        "color": "#f1f5f9"
    },
    {
        "id": 6,
        "title": "Harvester Park / IH Farm",
        "type": "Parks",
        "short": "Site of the world's first all-purpose tractor testing.",
        "description": "In 1917, International Harvester purchased 414 acres here for an experimental farm to test the 'Farmall' tractor. The village was so proud of this agricultural innovation that it was originally named 'Harvester' when it incorporated in 1956. Today, the park is a tribute to this legacy of local invention and agricultural science.",
        "date": "Established: 1917 / Park: 1980s",
        "color": "#ecfdf5"
    },
    {
        "id": 7,
        "title": "The Bridewell Prison Farm",
        "type": "History",
        "short": "A self-sufficient jail farm that shaped our Village Center.",
        "description": "From 1917 to 1969, the Cook County Prison Farm (The Bridewell) operated on land that now includes the Ambriance subdivision. Inmates produced dairy and crops for the county jail. After closing in 1969, the land's transition to residential use was a turning point for Burr Ridge, eventually becoming a site for high-end gated communities and the Village Center.",
        "date": "Operated: 1917-1969",
        "color": "#fef2f2"
    },
    {
        "id": 8,
        "title": "Highland Fields / Busby Farm",
        "type": "History",
        "short": "The dairy farm that gave Burr Ridge its name.",
        "description": "In the 1940s, Denver Busby established the 190-acre Burr Ridge Dairy Farm. Busby launched 'Burr Ridge Estates' with 5-acre lots, establishing the village's identity as a luxury residential community. His dairy farm name was adopted by the village upon incorporation, directly linking our modern name to his pastoral vision.",
        "date": "Heritage: 1940s",
        "color": "#fed7aa"
    },
    {
        "id": 9,
        "title": "Schustek Pond",
        "type": "Monuments",
        "short": "The heroic story of the 'Parachute Martyr' (1930).",
        "description": "On July 6, 1930, pilot Bruno Schustek died a hero while trying to rescue heiress Mary Fahrney, whose parachute had become entangled in his plane's wing. Schustek climbed onto the wing 1,000 feet in the air to free her, but tragically fell to his death. Fahrney survived. The pond near Veterans Blvd was officially named in his honor in 2015 on the 85th anniversary of the incident.",
        "date": "Incident: July 6, 1930 / Named: 2015",
        "color": "#dbeafe"
    },
    {
        "id": 10,
        "title": "Burr Ridge Veterans Memorial",
        "type": "Monuments",
        "short": "Honoring service members and Medal of Honor recipient Lester Weber.",
        "description": "Dedicated in 2010, this memorial features five walls representing the branches of the military and a 'Fallen Soldier' sculpture. It specifically honors local hero Lester W. Weber, a Burr Ridge Medal of Honor recipient from the Vietnam War. Over 700 engraved bricks and a gold dome make this one of the most prominent landmarks in the village.",
        "date": "Opened: June 2010",
        "color": "#fee2e2"
    },
    {
        "id": 11,
        "title": "The Dove Bar Factory",
        "type": "History",
        "short": "A sweet piece of local pride manufactured in Burr Ridge.",
        "description": "The world-famous Dove Bar ice cream treat has deep ties to the community. Originally invented in 1956 by Leo Stefanos at a candy shop in Chicago, the massive popularity of the treat led to a large manufacturing presence right here in Burr Ridge. It remains a point of local pride for residents who remember the bars being made in their own backyard.",
        "date": "Established: 1950s-1980s",
        "color": "#fef3c7"
    },
    {
        "id": 12,
        "title": "The Origin of 'Burr Ridge'",
        "type": "History",
        "short": "Named for the bur oak trees and glacial ridges.",
        "description": "The name 'Burr Ridge' was officially adopted due to the bur oak trees that grew along the high ridges of the community. These rolling hills were carved by glaciers during the last ice age, leaving the village situated primarily on the Valparaiso Moraine. The name reflects our unique natural landscape and the ancient environmental forces that shaped our land.",
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

# Header
st.markdown("# 📍 Village of Burr Ridge | History & Landmarks")
st.caption("Explore the stories behind our most significant commemorative sites")

# Hero Section
st.markdown("""
    <div class="hero-section">
        <h2>Preserving Our Local Legacy</h2>
        <p>Explore the stories behind our most significant landmarks—from the Potawatomi camps and early pioneers to the invention of the Dove Bar.</p>
    </div>
""", unsafe_allow_html=True)

# Search and Filter
col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input(
        "🔍 Search landmarks, names, or keywords...",
        value=st.session_state.search_query,
        key="search_input"
    )
    st.session_state.search_query = search_query

with col2:
    filter_type = st.selectbox(
        "Filter by Category",
        ["All", "History", "Parks", "Monuments"],
        index=["All", "History", "Parks", "Monuments"].index(st.session_state.current_filter)
    )
    st.session_state.current_filter = filter_type

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
                    <h4 style="margin-top: 0; margin-bottom: 0.5rem;">{landmark['title']}</h4>
                    <p style="color: #64748b; font-size: 0.95rem; margin: 1rem 0;">{landmark['short']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("View Details", key=f"btn_{landmark['id']}", use_container_width=True):
                st.session_state.selected_landmark = landmark
                st.rerun()
else:
    st.info("📭 No landmarks found matching your search.")

# Detail Modal
if st.session_state.selected_landmark:
    landmark = st.session_state.selected_landmark
    
    st.markdown("---")
    col1, col2 = st.columns([10, 1])
    with col2:
        if st.button("✕", key="close_modal"):
            st.session_state.selected_landmark = None
            st.rerun()
    
    st.markdown(f"<div class='category-badge'>{landmark['type']}</div>", unsafe_allow_html=True)
    st.markdown(f"## {landmark['title']}")
    
    st.markdown("---")
    st.write(landmark["description"])
    
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption(f"🕐 {landmark['date']}")
    with col2:
        if st.button("View on Map", use_container_width=True):
            st.info("🗺️ Map integration coming soon!")

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
    if st.button("📝 Submit a Story", use_container_width=True):
        st.session_state.show_suggest_modal = True
        st.rerun()

# Suggestion Form Modal
if st.session_state.show_suggest_modal:
    st.markdown("---")
    st.markdown("## 📝 Suggest a Landmark")
    st.caption("Contribute to the Burr Ridge archive.")
    
    with st.form("suggest_form"):
        landmark_name = st.text_input("Landmark or Location Name *", placeholder="Enter the name...")
        story = st.text_area("The Story / Historical Context *", placeholder="Who is it named after? Why is it important?", height=150)
        photo_url = st.text_input("Upload Photo (Optional URL)", placeholder="Link to an image if available...")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button("Submit to Historical Society", use_container_width=True)
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.show_suggest_modal = False
                st.rerun()
        
        if submitted:
            if landmark_name and story:
                st.success("✅ Thank you! Your submission has been received.")
                st.session_state.show_suggest_modal = False
                st.balloons()
            else:
                st.error("Please fill in all required fields marked with *")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.caption("© 2026 Village of Burr Ridge, Illinois. All rights reserved.")
with col2:
    st.caption("[Contact](mailto:history@burr-ridge.org)")
with col3:
    st.caption("[About](#)")
