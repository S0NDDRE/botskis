"""
Mindframe AI Course Assistant
Your personal AI mentor that guides you through courses

Features:
- Explains concepts in simple terms
- Answers questions about lessons
- Provides hints for exercises
- Encourages and motivates
- Adapts to your learning style
- Remembers your progress
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from openai import AsyncOpenAI
from loguru import logger
import json


class AssistantMessage(BaseModel):
    """AI Assistant message"""
    message: str
    type: str  # "explanation", "hint", "encouragement", "correction", "next_step"
    suggested_actions: List[str] = []  # What user can do next
    resources: List[Dict] = []  # Additional resources


class LearningContext(BaseModel):
    """Current learning context"""
    user_name: str
    course_title: str
    lesson_title: str
    lesson_type: str
    user_level: str  # laerling, junior, etc.
    current_progress: float  # 0-100%
    previous_lessons_completed: List[str]
    struggles_with: List[str] = []  # Topics user finds difficult
    learning_style: str = "visual"  # visual, hands-on, theoretical


class MindframeAICourseAssistant:
    """
    AI Course Assistant - Your Personal Learning Mentor

    Personality:
    - Friendly and encouraging
    - Patient and understanding
    - Explains things simply
    - Uses examples from Mindframe
    - Celebrates progress
    """

    def __init__(self, openai_api_key: str):
        self.client = AsyncOpenAI(api_key=openai_api_key)
        self.model = "gpt-4-turbo-preview"

    async def answer_question(
        self,
        question: str,
        context: LearningContext
    ) -> AssistantMessage:
        """
        Answer student's question about the course

        The AI adapts its answer based on:
        - User's level (Lærling vs CEO)
        - Current lesson context
        - Learning style
        - Previous struggles
        """
        logger.info(f"🎓 AI Assistant answering: {question}")

        # Build system prompt based on context
        system_prompt = self._build_system_prompt(context)

        # Build user prompt
        user_prompt = f"""
Student Question: "{question}"

Current Lesson: {context.lesson_title}
Lesson Type: {context.lesson_type}
Progress: {context.current_progress}%

Please provide:
1. A clear, friendly answer
2. Practical examples from Mindframe platform
3. 2-3 suggested next actions
4. Any helpful resources

Remember: Keep it simple and encouraging!
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            result = json.loads(response.choices[0].message.content)

            return AssistantMessage(
                message=result.get("answer", ""),
                type="explanation",
                suggested_actions=result.get("suggested_actions", []),
                resources=result.get("resources", [])
            )

        except Exception as e:
            logger.error(f"AI Assistant error: {e}")
            return AssistantMessage(
                message="Hmm, jeg hadde litt problemer med å svare. Kan du prøve igjen?",
                type="error",
                suggested_actions=["Prøv å omformulere spørsmålet"]
            )

    async def provide_hint(
        self,
        exercise: Dict,
        user_attempt: Any,
        context: LearningContext
    ) -> AssistantMessage:
        """
        Provide a hint for an exercise (without giving full answer)

        Smart hints:
        - First hint: Gentle nudge
        - Second hint: More specific
        - Third hint: Almost the answer
        """
        logger.info(f"💡 Providing hint for exercise")

        prompt = f"""
User is stuck on an exercise:

Exercise: {exercise.get('title')}
Description: {exercise.get('description')}

User's attempt: {user_attempt}

Provide a helpful hint WITHOUT giving the full answer.

Return JSON:
{{
    "hint": "Friendly hint message",
    "type": "hint",
    "suggested_actions": ["Try this...", "Check..."],
    "should_reveal_more": false
}}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a patient teacher. Give hints, not answers."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            result = json.loads(response.choices[0].message.content)

            return AssistantMessage(
                message=result.get("hint", ""),
                type="hint",
                suggested_actions=result.get("suggested_actions", [])
            )

        except Exception as e:
            logger.error(f"Hint generation error: {e}")
            return AssistantMessage(
                message="Prøv å bryte ned problemet i mindre deler!",
                type="hint"
            )

    async def explain_concept(
        self,
        concept: str,
        context: LearningContext
    ) -> AssistantMessage:
        """
        Explain a concept in simple terms with Mindframe examples

        Adapts explanation to user level:
        - Lærling: Very simple, lots of examples
        - Junior: Intermediate, practical
        - Senior: Technical details
        - CEO: Business impact, strategy
        """
        logger.info(f"📚 Explaining concept: {concept}")

        system_prompt = self._build_system_prompt(context)

        prompt = f"""
Explain this concept: "{concept}"

Adapt your explanation for a {context.user_level} level user.

Lærling: Use very simple language, everyday examples
Junior: Practical examples, how-to focus
Medior/Senior: Technical details, best practices
Manager/CEO: Business value, strategic importance

Always include:
- What it is (simple definition)
- Why it matters (real benefit)
- How to use it in Mindframe
- Real example

Return JSON:
{{
    "explanation": "Clear explanation...",
    "example": "Practical Mindframe example...",
    "why_it_matters": "Business value...",
    "type": "explanation",
    "suggested_actions": ["Try this...", "Learn more..."]
}}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            result = json.loads(response.choices[0].message.content)

            explanation = f"{result.get('explanation', '')}\n\n"
            explanation += f"**Hvorfor det betyr noe:** {result.get('why_it_matters', '')}\n\n"
            explanation += f"**Eksempel:** {result.get('example', '')}"

            return AssistantMessage(
                message=explanation,
                type="explanation",
                suggested_actions=result.get("suggested_actions", [])
            )

        except Exception as e:
            logger.error(f"Concept explanation error: {e}")
            return AssistantMessage(
                message=f"La meg forklare {concept} på en enkel måte...",
                type="explanation"
            )

    async def check_quiz_answer(
        self,
        question: Dict,
        user_answer: Any,
        context: LearningContext
    ) -> AssistantMessage:
        """
        Check quiz answer and provide feedback

        Feedback types:
        - Correct: Celebrate and explain why
        - Incorrect: Gently correct and explain
        - Partial: Acknowledge what's right, guide to complete answer
        """
        logger.info(f"✅ Checking quiz answer")

        correct_answer = question.get("correct_answer")
        is_correct = str(user_answer).lower() == str(correct_answer).lower()

        prompt = f"""
Question: {question.get('question')}
User's Answer: {user_answer}
Correct Answer: {correct_answer}
Is Correct: {is_correct}

Provide encouraging feedback.

If correct:
- Celebrate!
- Briefly explain why it's right
- Encourage to continue

If incorrect:
- Be gentle and encouraging
- Explain what the correct answer is and WHY
- Don't make them feel bad
- Suggest reviewing specific concept

Return JSON:
{{
    "feedback": "Encouraging message...",
    "explanation": "Why this answer is correct/incorrect...",
    "type": "correction" or "encouragement",
    "suggested_actions": ["Review...", "Try..."]
}}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an encouraging teacher. Celebrate success, gently correct mistakes."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            result = json.loads(response.choices[0].message.content)

            message = f"{result.get('feedback', '')}\n\n{result.get('explanation', '')}"

            return AssistantMessage(
                message=message,
                type=result.get('type', 'correction'),
                suggested_actions=result.get('suggested_actions', [])
            )

        except Exception as e:
            logger.error(f"Quiz feedback error: {e}")

            if is_correct:
                return AssistantMessage(
                    message="🎉 Riktig! Flott jobbet!",
                    type="encouragement"
                )
            else:
                return AssistantMessage(
                    message=f"Ikke helt! Det riktige svaret er: {correct_answer}. Prøv igjen!",
                    type="correction"
                )

    async def suggest_next_step(
        self,
        context: LearningContext
    ) -> AssistantMessage:
        """
        Suggest what to do next based on progress

        Suggestions:
        - Continue to next lesson
        - Review challenging topics
        - Take a quiz to test knowledge
        - Try a hands-on exercise
        - Take a break (if studying too long)
        """
        logger.info(f"🚀 Suggesting next step")

        prompt = f"""
Student Progress:
- Current Course: {context.course_title}
- Current Lesson: {context.lesson_title}
- Progress: {context.current_progress}%
- Level: {context.user_level}
- Completed Lessons: {len(context.previous_lessons_completed)}
- Struggles with: {', '.join(context.struggles_with) if context.struggles_with else 'Nothing yet'}

Based on this, suggest the BEST next action.

Consider:
- If stuck on something → suggest review or different approach
- If doing well → encourage to continue
- If completed many lessons → suggest quiz or break
- If struggling → suggest easier exercises or review

Return JSON:
{{
    "suggestion": "Friendly suggestion...",
    "reasoning": "Why this is a good next step...",
    "type": "next_step",
    "suggested_actions": ["Continue to next lesson", "Review X", "Take quiz"]
}}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a learning advisor. Suggest the best next step for the student."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )

            result = json.loads(response.choices[0].message.content)

            return AssistantMessage(
                message=f"{result.get('suggestion', '')}\n\n{result.get('reasoning', '')}",
                type="next_step",
                suggested_actions=result.get('suggested_actions', [])
            )

        except Exception as e:
            logger.error(f"Next step suggestion error: {e}")
            return AssistantMessage(
                message="La oss fortsette! Klar for neste leksjon?",
                type="next_step",
                suggested_actions=["Fortsett til neste leksjon"]
            )

    def _build_system_prompt(self, context: LearningContext) -> str:
        """Build context-aware system prompt"""

        level_prompts = {
            "laerling": "You are teaching a complete beginner. Use VERY simple language. Lots of examples. No jargon.",
            "junior": "You are teaching someone with basic knowledge. Use practical examples. Some technical terms OK.",
            "medior": "You are teaching an intermediate user. Technical detail welcome. Focus on best practices.",
            "senior": "You are teaching an advanced user. Deep technical details. Discuss edge cases and optimization.",
            "lead": "You are teaching a team lead. Focus on leadership, delegation, and team efficiency.",
            "manager": "You are teaching a manager. Focus on ROI, metrics, business impact, and strategy.",
            "director": "You are teaching a director. Focus on vision, scaling, competitive advantage.",
            "ceo": "You are teaching a CEO. Focus on business transformation, market domination, strategic vision."
        }

        system_prompt = f"""You are the Mindframe AI Course Assistant - a friendly, patient, and encouraging mentor.

Student Level: {context.user_level}
{level_prompts.get(context.user_level, level_prompts['laerling'])}

Student Name: {context.user_name}
Learning Style: {context.learning_style}

Your role:
- Answer questions clearly
- Provide practical Mindframe examples
- Encourage and celebrate progress
- Be patient with mistakes
- Adapt explanations to user's level
- Make learning fun!

Always:
- Use Norwegian when appropriate (student prefers it)
- Include practical Mindframe platform examples
- Provide actionable next steps
- Be encouraging and positive

Never:
- Be condescending
- Give up on the student
- Provide wrong information
- Skip important details
"""

        return system_prompt


# Usage Example
async def example_usage():
    """Example of AI Course Assistant in action"""

    assistant = MindframeAICourseAssistant(openai_api_key="your-key")

    # Student context
    context = LearningContext(
        user_name="Anders",
        course_title="Mindframe for Beginners",
        lesson_title="Creating Your First AI Agent",
        lesson_type="interactive",
        user_level="laerling",
        current_progress=45.0,
        previous_lessons_completed=["intro", "platform_tour"],
        learning_style="hands-on"
    )

    # 1. Student asks a question
    answer = await assistant.answer_question(
        question="Hva er forskjellen på AI Agent og Voice AI?",
        context=context
    )
    print(f"🤖 Assistant: {answer.message}")
    print(f"Suggested actions: {answer.suggested_actions}")

    # 2. Student stuck on exercise - needs hint
    exercise = {
        "title": "Create Email Automation Agent",
        "description": "Build an agent that responds to customer emails"
    }
    hint = await assistant.provide_hint(
        exercise=exercise,
        user_attempt="I don't know where to start...",
        context=context
    )
    print(f"\n💡 Hint: {hint.message}")

    # 3. Explain a concept
    explanation = await assistant.explain_concept(
        concept="Meta-AI Guardian",
        context=context
    )
    print(f"\n📚 Explanation: {explanation.message}")

    # 4. Check quiz answer
    question = {
        "question": "What does AI Agent Generator do?",
        "correct_answer": "Creates configured agents from natural language"
    }
    feedback = await assistant.check_quiz_answer(
        question=question,
        user_answer="Creates agents automatically",
        context=context
    )
    print(f"\n✅ Feedback: {feedback.message}")

    # 5. Suggest next step
    next_step = await assistant.suggest_next_step(context=context)
    print(f"\n🚀 Next: {next_step.message}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
