def calculate_relevance_score(job, user_input):
    """
    Calculates a relevance score (0-100) based on how well the job matches the user input.
    """
    if not user_input or not isinstance(user_input, str):
        return 0
        
    score = 0
    user_keywords = [word.lower().strip(",.") for word in user_input.split() if len(word) > 2]
    
    if not user_keywords:
        return 0
        
    title = job.get('title', '').lower()
    description = job.get('description', '').lower()
    skills_required = [s.lower() for s in job.get('skills_required', [])]
    
    max_possible_score = len(user_keywords) * 15 # 15 points max per keyword
    
    for word in user_keywords:
        # Match in Title (High weight)
        if word in title:
            score += 10
        # Match in explicitly required skills (High weight)
        elif any(word in skill for skill in skills_required):
            score += 10
        # Match in description (Lower weight)
        elif word in description:
            score += 5
            
    # Normalize score to 0-100
    normalized_score = min(int((score / max_possible_score) * 100), 100) if max_possible_score > 0 else 0
    
    # Give a base score if there was at least some overlap, to ensure it doesn't completely fail
    # if the math above is too strict, but for now we just return the normalized score.
    
    return normalized_score
