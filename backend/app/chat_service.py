import os
import re
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .models import ChatMode

# Profanity filter for regular mode
PROFANITY_WORDS = [
    "damn", "hell", "shit", "fuck", "bitch", "ass", "bastard", "crap",
    "piss", "cock", "dick", "pussy", "whore", "slut", "fag", "nigger",
    "retard", "gay", "lesbian", "homo", "queer", "tranny"
]

class ChatService:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.7,
            groq_api_key=self.groq_api_key,
            max_tokens=1024
        )
        
        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{user_input}")
        ])
        
        self.chain = self.prompt_template | self.llm

    def _get_system_prompt(self) -> str:
        return """You are {persona}. 

Mode: {mode}

Instructions:
- Stay completely in character as the persona described
- Respond in a way that matches the persona's personality, speech patterns, and worldview
- If in regular mode, keep responses family-friendly and appropriate
- If in uncensored mode, you can be more creative and edgy while still being helpful
- Make your responses engaging, entertaining, and true to the character
- Don't break character or mention that you're an AI unless it's part of your persona
- Keep responses conversational and not too long (2-3 sentences typically)

Remember: You ARE this persona, not an AI pretending to be them."""

    def _apply_profanity_filter(self, text: str) -> tuple[str, bool]:
        """Apply profanity filter to text. Returns (filtered_text, was_filtered)"""
        original_text = text
        filtered = False
        
        for word in PROFANITY_WORDS:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            if pattern.search(text):
                filtered = True
                # Replace with asterisks, keeping first and last letter
                if len(word) > 2:
                    replacement = word[0] + "*" * (len(word) - 2) + word[-1]
                else:
                    replacement = "*" * len(word)
                text = pattern.sub(replacement, text)
        
        return text, filtered

    def _build_conversation_history(self, history: List[Dict[str, Any]], persona: str) -> List:
        """Build conversation history for context"""
        messages = []
        
        for entry in history[-10:]:  # Keep last 10 messages for context
            if entry.get("type") == "human":
                messages.append(HumanMessage(content=entry["content"]))
            elif entry.get("type") == "ai":
                messages.append(AIMessage(content=entry["content"]))
        
        return messages

    async def generate_response(
        self, 
        user_input: str, 
        persona: str, 
        mode: ChatMode,
        conversation_history: List[Dict[str, Any]] = None
    ) -> tuple[str, bool]:
        """Generate a response using the ChatGroq model"""
        
        if conversation_history is None:
            conversation_history = []
        
        try:
            # Format the prompt with persona and mode
            mode_text = "regular (family-friendly)" if mode == ChatMode.REGULAR else "uncensored (creative)"
            
            # Create the full prompt
            system_prompt = self._get_system_prompt().format(
                persona=persona,
                mode=mode_text
            )
            
            # Build messages including conversation history
            messages = [SystemMessage(content=system_prompt)]
            
            # Add conversation history
            history_messages = self._build_conversation_history(conversation_history, persona)
            messages.extend(history_messages)
            
            # Add current user input
            messages.append(HumanMessage(content=user_input))
            
            # Generate response
            response = await self.llm.ainvoke(messages)
            response_text = response.content
            
            # Apply profanity filter if in regular mode
            filtered = False
            if mode == ChatMode.REGULAR:
                response_text, filtered = self._apply_profanity_filter(response_text)
            
            return response_text, filtered
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            if mode == ChatMode.REGULAR:
                error_msg, _ = self._apply_profanity_filter(error_msg)
            return error_msg, False

    def validate_persona(self, persona: str) -> bool:
        """Validate that persona description is appropriate"""
        if not persona or len(persona.strip()) < 10:
            return False
        
        # Check for inappropriate content in persona description
        inappropriate_terms = [
            "sexual", "explicit", "nsfw", "porn", "nude", "naked",
            "violence", "kill", "murder", "suicide", "self-harm",
            "illegal", "drugs", "weapons", "bomb", "terrorist"
        ]
        
        persona_lower = persona.lower()
        for term in inappropriate_terms:
            if term in persona_lower:
                return False
        
        return True
