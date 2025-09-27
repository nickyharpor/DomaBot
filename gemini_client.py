from typing import Optional
import google.generativeai as genai


class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        """
        Initialize the GeminiClient with an API key and model.
        :param api_key: Your Google AI Studio API key
        :param model: The Gemini model to use (default: gemini-2.0-flash)
        """
        genai.configure(api_key=api_key)
        self.model = model

    def generate_response(self, user_input: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the Gemini model.
        :param user_input: The user query/input text
        :param system_prompt: Optional system instruction for the model
        :return: The model's text response
        """
        try:
            model = genai.GenerativeModel(self.model)

            # If a system prompt is provided, prepend it to user input
            final_input = user_input
            if system_prompt:
                final_input = f"{system_prompt}\n\nUser prompt: {user_input}"

            # Generate response (just one user role, no system role allowed)
            response = model.generate_content([{"role": "user", "parts": [{"text": final_input}]}])

            return response.text if response and response.text else "[No response received]"

        except Exception as e:
            return f"Error: {str(e)}"


    def gen_augment_keyword(self, user_prompt):
        system_prompt = '''Your job is to suggest up to 10 keywords to be used as a domain name.
        You only respond with the keywords (space-separated). Only the keywords, nothing else.
        Up to 10 words as the keyword to search for domain names, in space-separated format.
        No matter the user prompt language, keywords must be in English and lowercase.
        '''
        ai_response = self.generate_response(user_prompt, system_prompt)
        if ai_response:
            ai_keywords_list = ai_response.split()
            if len(ai_keywords_list) > 10:
                ai_keywords_list = ai_keywords_list[:10]
        else:
            ai_keywords_list = []
        return ai_keywords_list


    def gen_suggest_domain(self, user_prompt, domain_list):
        system_prompt = f'''Based on the list of domains below, suggest up to 10 of the best domains.
        Domain list: {str(domain_list)}
        Your response MUST be only up to 10 space-separated domain names from the above list. Nothing else.
        Find the best domains among all based on the user prompt.'''
        ai_response = self.generate_response(user_prompt, system_prompt)
        if ai_response:
            ai_domains_list = ai_response.split()
            if len(ai_domains_list) > 10:
                ai_domains_list = ai_domains_list[:10]
        else:
            ai_domains_list = []
        ai_domains_list_purified = []
        for d in ai_domains_list:
            if '.' in d and len(d) > 4:
                ai_domains_list_purified.append(d)
        return ai_domains_list_purified


