from crewai import Task
from textwrap import dedent

class TripTasks:

    def gather_task(self, agent, start_city, destination_city, interests, start_date, end_date):
        return Task(
            description=dedent(f"""
            As a trusted local expert of **{destination_city}**, your task is to create a high-value city guide for a traveler coming from **{start_city}**, planning a trip between **{start_date}** and **{end_date}**, and interested in: **{interests}**.
            Provide a rich overview of the destination, including:
            - 🌍 Key attractions and iconic landmarks
            - 🔍 Hidden gems that only locals know
            - 🧭 Neighborhoods worth exploring and why
            - 🎭 Cultural norms, traditions, local etiquette
            - 📅 Events or festivals happening during the travel dates
            - 🌤️ Weather forecast during that time
            - 💸 High-level cost estimates for travelers
            - 🛡️ Basic travel safety tips and customs
            Your guide should feel like a local’s cheat sheet — detailed, culturally rich, and practically helpful.
            """),
            agent=agent,
            expected_output="Comprehensive city guide including hidden gems, cultural hotspots, and practical travel tips"
        )

    def plan_task(self, agent, start_city, destination_city, interests, start_date, end_date):
        trip_duration = (end_date - start_date).days + 1
        return Task(
            description=dedent(f"""
You are a world-class travel planner. Create a **complete {trip_duration}-day itinerary** for a traveler going from **{start_city}** to **{destination_city}**, between **{start_date.strftime('%B %d, %Y')}** and **{end_date.strftime('%B %d, %Y')}**.  
**Traveler Interests:** {', '.join(interests) if isinstance(interests, list) else interests}

You must **STRICTLY follow this structure and content rules below. Do not skip, merge or move sections. Do not provide links unless specified.**

---

## 📅 Daily Structure (MANDATORY PER DAY)
For each day (e.g., **## Day 1**, **## Day 2**, etc.), include:
- 🌤️ Weather forecast (temperature range and rain chance)
- 🗺️ **3 actual places to visit**, with 1-line reason for each — **do not provide links**
- 🍴 Name **1–2 local restaurants or cafés** — **do not include links**
- 🛏️ Name **1 mid-to-luxury hotel** — **no booking links**
- ✈️ Flight info (ONLY on Day 1 and Last Day as described below)
- 🚕 Local transport suggestion (cab/rental/mid-luxury options)
- 🎒 Daily packing tip based on weather

---

## ✈️ Flight Options (IndiGo only — **MANDATORY format**)

Only on:
- **Day 1**: Provide **onward** flight
- **Last Day**: Provide **return** flight

Format flights as a markdown table:

| Flight        | Time     | Price  | Link                                        |
|---------------|----------|--------|---------------------------------------------|
| IndiGo 6E-123 | 7:45 AM  | ₹5,234 | [Book Now](https://www.makemytrip.com/flights/) |

**Use only MakeMyTrip flight links and only for IndiGo. No placeholder or generated URLs.**

---
## 💰 Budget Breakdown (FINAL SECTION BEFORE TRAVEL TIPS — USE REAL NUMBERS ONLY)

Create a **summary table** (NOT daily breakdown). Do **NOT** return any placeholder like ₹X or leave blank.

| Item          | Estimated Cost |
|---------------|----------------|
| Flights       | ₹9,200         |
| Accommodation | ₹18,000        |
| Food          | ₹6,000         |
| Transport     | ₹5,000         |
| Activities    | ₹3,500         |
| **Total**     | ₹41,700        |

**Rules:**
- Use realistic **mid-to-luxury pricing**
- **Flight cost must include BOTH onward and return IndiGo flights combined**
- Minimum combined budget for food and transport: ₹2,000/day
- Show numerical values for all rows. Do **not omit, skip, or leave any row blank**

---

## 🛡️ Must-Know Travel Tips (**Last section**)
List 3–5 practical, destination-specific travel tips:
- Cultural do’s and don’ts
- Hidden gems or local customs
- Safety tips
- What locals wish tourists knew

---

## 🔧 Output & Formatting Rules
- Structure output in clean **Markdown**
- Use **emojis** for headers and bullets
- **Include royalty-free image URLs** per day (for places/tips) — don't generate images
- Use **tables** for flights and budget breakdown only
- Do not merge or rearrange sections
- Avoid repetition or generic content

---

🧠 Imagine this is for a premium concierge travel app. Keep it vivid, useful, and realistic. Be consistent with structure across all trips.

            """),
            agent=agent,
            expected_output=f"Complete {trip_duration}-day expanded travel plan with daily schedule, weather conditions,Placed to visit, restaurants, hotel suggestions, flight options, mid to luxury transport recommendations, packing suggestions. budget breakdown for entire trip duration, travel tips"
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you 100"
