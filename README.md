# Burr Ridge Shared History - Streamlit Edition

An interactive web application showcasing commemorative landmarks and historical sites in the Village of Burr Ridge, Illinois.

## Features

- 📍 **12 Fact-Checked Landmarks** - History, Parks, and Monuments
- 🔍 **Search & Filter** - Real-time search across all landmarks
- 📖 **Detailed Narratives** - Rich historical context for each location
- 💬 **Community Contributions** - Submit new historical stories
- 📱 **Responsive Design** - Works on desktop and mobile devices

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nabilahaahim14/Burr-Ridge-Shared-History.git
cd Burr-Ridge-Shared-History
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Project Structure

```
Burr-Ridge-Shared-History/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

## Landmarks Included

1. **Potawatomi Last Camp Site** - 1835 historical marker
2. **Joseph Vial Log Cabin Site** - First post office and hotel (1834)
3. **Robert Vial House** - Oldest standing building (1856)
4. **Flagg Creek Heritage Museum** - Local history repository
5. **Hiram McClintock Civil War Letters** - Civil War era correspondence
6. **Harvester Park / IH Farm** - International Harvester experimental farm
7. **The Bridewell Prison Farm** - Historic prison farm (1917-1969)
8. **Highland Fields / Busby Farm** - Dairy farm origin of village name
9. **Schustek Pond** - Memorial to heroic pilot Bruno Schustek (1930)
10. **Burr Ridge Veterans Memorial** - Military tribute featuring Medal of Honor recipient
11. **The Dove Bar Factory** - Manufacturing site of famous ice cream treat
12. **The Origin of 'Burr Ridge'** - Named for bur oak trees and glacial ridges

## Features

### Search & Filter
- Search landmarks by name, description, or keywords
- Filter by category: All, History, Parks, Monuments
- Real-time results update

### Landmark Details
- Full historical narrative
- Category badges
- Dates and historical context
- Interactive modals for deeper exploration

### Community Submissions
- Submit new landmark stories
- Optional photo URL support
- Contribution confirmation

## Customization

### Adding New Landmarks

Edit the `LANDMARKS` list in `app.py` to add new entries:

```python
{
    "id": 13,
    "title": "Your Landmark Name",
    "type": "History",  # or "Parks", "Monuments"
    "short": "Brief description",
    "description": "Full historical narrative...",
    "date": "Date or era",
    "color": "#hexcolor"
}
```

### Styling

Customize colors and appearance by modifying:
- `.streamlit/config.toml` - Theme colors
- CSS in the `<style>` block in `app.py`

## Contributing

We welcome community contributions! Please submit historical stories and corrections through the "Submit a Story" feature in the app.

## License

All content is © 2026 Village of Burr Ridge, Illinois. All rights reserved.

## Support

For questions or issues, please open an issue on GitHub.
