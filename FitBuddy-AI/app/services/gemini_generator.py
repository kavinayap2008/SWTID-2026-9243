from ..config import get_settings
from .gemini_client import generate_text


# ---------------------------------------------------------
# MOCK WORKOUT
# ---------------------------------------------------------

def _mock_plan(
    goal: str,
    intensity: str,
) -> str:

    return f"""
7-Day FitBuddy Workout Plan

Goal: {goal}
Intensity: {intensity.title()}


Day 1 – Full Body Foundation

Warm-up:
7 minutes brisk walking and mobility exercises.

Main Workout:
• Squats - 3 sets x 10 reps
• Incline Push-ups - 3 sets x 10 reps
• Dumbbell/Resistance Rows - 3 sets x 12 reps
• Glute Bridges - 3 sets x 12 reps

Cooldown:
5 minutes easy stretching.


Day 2 – Cardio & Core

Warm-up:
5 minutes easy movement.

Main Workout:
• 25 minutes steady-state cardio
• Dead Bug - 3 sets x 10 per side
• Plank - 3 sets x 30 seconds
• Bird Dog - 3 sets x 10 per side

Cooldown:
Slow walking and breathing exercises.


Day 3 – Recovery & Mobility

• 30-minute easy walk
• 15-minute full-body mobility session
• Gentle stretching
• Focus on hydration and recovery


Day 4 – Lower Body

Warm-up:
8 minutes dynamic mobility.

Main Workout:
• Split Squats - 3 sets x 8 per side
• Hip Hinge - 3 sets x 10
• Step-ups - 3 sets x 10 per side
• Calf Raises - 3 sets x 15

Cooldown:
5-10 minutes stretching.


Day 5 – Upper Body

Warm-up:
Arm circles and light cardio.

Main Workout:
• Push-ups - 3 sets x 8-12 reps
• Rows - 3 sets x 10-12 reps
• Shoulder Press - 3 sets x 10 reps
• Bird Dog - 3 sets x 10 per side

Cooldown:
Chest, shoulder and back stretches.


Day 6 – Conditioning

Warm-up:
5 minutes easy cardio.

Main Workout:

30 minutes of intervals:

• 2 minutes moderate exercise
• 1 minute easy recovery

Repeat according to your fitness level.

Cooldown:
5 minutes easy walking.


Day 7 – Rest & Recovery

• Complete rest or gentle walking
• Hydrate adequately
• Prioritize quality sleep
• Perform optional gentle stretching


Safety Note:

Stop exercising if you experience chest pain, faintness,
severe shortness of breath or sharp pain.

This workout is general fitness information and is not
a substitute for professional medical advice.
""".strip()


# ---------------------------------------------------------
# GEMINI WORKOUT GENERATION
# ---------------------------------------------------------

def generate_workout_gemini(
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:

    settings = get_settings()

    # -----------------------------------
    # MOCK MODE
    # -----------------------------------

    if settings.mock_ai:

        return _mock_plan(
            goal,
            intensity,
        )

    # -----------------------------------
    # GEMINI PROMPT
    # -----------------------------------

    prompt = f"""
You are FitBuddy, a careful and practical fitness planning assistant.

Create a personalized 7-day workout plan for the following user.

USER INFORMATION

Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Preferred Workout Intensity: {intensity}

REQUIREMENTS

1. Create exactly 7 days.

2. Label the sections:

Day 1
Day 2
Day 3
Day 4
Day 5
Day 6
Day 7

3. Each workout day should contain:

Warm-up:
5-10 minutes.

Main Workout:
Provide exercise names.

Include:
- sets
- repetitions
OR
- exercise duration

Also include sensible rest periods when appropriate.

Cooldown:
Provide stretching, mobility or recovery recommendations.

4. Include at least one rest or active-recovery day.

5. Adapt the overall difficulty according to the user's
preferred intensity:

Low
Medium
High

6. Align the exercises with this goal:

{goal}

7. Prefer common home or gym exercises.

8. Provide simple substitutions where useful.

9. Do not diagnose medical conditions.

10. Do not guarantee weight loss, muscle gain or any
specific health outcome.

11. Finish with a short safety note.

12. Return plain text.

13. Do NOT create a Markdown table.

Make the workout easy to read and practical.
"""

    return generate_text(
        settings.gemini_workout_model,
        prompt,
    )