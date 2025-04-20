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
            You are a world-class travel planner. Your task is to create a **complete {trip_duration}-day itinerary** for a traveler going from **{start_city}** to **{destination_city}**, from **{start_date.strftime('%B %d, %Y')}** to **{end_date.strftime('%B %d, %Y')}**.
            This itinerary must include:
            - 📅 Clear daily structure (Day 1, Day 2, etc.) Day Wise Itinerary
            - 🌤️ Approximate daily weather forecast
            - 🗺️ Specific places to visit each day (with short why it's special) 
            - 🍴 Local restaurants or cafés (name ) 
            - 🛏️ **Hotel suggestions** (preferably Mid to luxury range, do not provide booking links )
            - ✈️ **Flight options(only Indigo) with booking site links** (e.g., from MakeMyTrip)
            - 🚕 Local transport recommendations (e.g., only Uber link)
            - 🎒 Daily packing tips based on weather
            - 💰 Full **budget breakdown** (stay, food, transport, tickets, etc.) include both onward and return flight tickets budget, pick the cost from the above suggestions
            Format the result in clear Markdown with colorful images:
            - Headings (e.g. ## Day 1, Day2, Day3..., ## Budget Breakdown)
            - appropriate colorful images for locations and tips
            - Tables for budget and accommodations (if applicable)
            Make it feel exclusive and realistic, include beautiful heart touching images, — as if you're planning a trip for a premium travel app.               
            """),
            agent=agent,
            expected_output=f"Complete {trip_duration}-day expanded travel plan with daily schedule, weather conditions,Placed to visit, restaurants, hotel suggestions, flight options, local transport recommendations, packing suggestions, and budget breakdown"
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you 100"
