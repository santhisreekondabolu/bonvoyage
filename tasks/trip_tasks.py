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

Your itinerary **must include the following elements**:

### 📅 Daily Structure
- Day-wise plan (e.g., **## Day 1**, **## Day 2**...)
- 🌤️ Approximate weather for each day
- 🗺️ **Actual** places to visit with a short reason why it’s special (**no links**)
- 🍴 Names of local restaurants/cafés (**no links**)
- 🛏️ Mid-to-luxury hotel suggestions (**no booking links**)

### ✈️ Flight Options (IndiGo only)
- Include **actual** flight name, time, price, and a booking link from MakeMyTrip
- Add flights as a **table**, like:


Flight	Time	Price	Link
IndiGo 6E-123	7:45 AM	₹5,234	Book Now
yaml
Copy
Edit

- Day 1 must include **onward** flight  
- Last day must include **return** flight

### 🚕 Local Transport
- Mention mid-to-luxury local transport options (cab, rental, etc.)

### 🎒 Packing Tips
- Based on forecasted weather, give **daily tips** on what to pack

### 💰 Budget Breakdown
- End with a **summary table** (not per day, but for entire trip)
- Budget must include flight (inbound & return), stay, food, transport, activities
- Minimum of ₹2,000/day for food + transport (mid to luxury range)

---

### 🛡️ Must-Know Travel Tips (This section **must appear at the end**)
- Cultural etiquette
- Hidden gems
- Safety or insider advice
- Keep tips practical and destination-specific

---

### 🔧 Formatting Requirements
- Output should be **clear Markdown**
- Use emojis for sections
- Include **images** that visually enhance the guide (use image URLs, don't generate them)
- Tables for flight and budget info (avoid raw bullet points)

---

Make it feel like a **premium itinerary for a travel app**, blending utility with visual appeal.               
            """),
            agent=agent,
            expected_output=f"Complete {trip_duration}-day expanded travel plan with daily schedule, weather conditions,Placed to visit, restaurants, hotel suggestions, flight options, mid to luxury transport recommendations, packing suggestions. budget breakdown for entire trip duration, travel tips"
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you 100"
