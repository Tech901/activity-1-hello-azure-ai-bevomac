# Reflection -- Hello, Azure AI

Answer these questions after completing the activity (2-3 sentences each). Connect your answers to specific things you observed while coding and experimenting.

## 1. Service Surprises

Which of the three Azure AI services (OpenAI, Content Safety, Language) surprised you the most? Connect this to something specific you observed during your experiments -- a response you didn't expect, a behavior that seemed too easy or too hard, or a result that made you rethink how the service works.

It wasn't hard to get the complaints to change and be the correct category. The temperature, no matter what i changed it to, gave it a confidence of 0.95. Removing the category list, it still gave Noise complaint, and Pothole repair as the caterories, correctly. 

## 2. Lazy Initialization

How would you explain the lazy initialization pattern to a colleague? Why is it used instead of creating clients at the top of the file?

With the lazy initialization, you wait and create the client when you actually need it instead of the moment the file loads. This prevents errors and crashes when it tries to connect too early. If it's never called, it's never created.

## 3. Content Safety in the Real World

A resident files this complaint: *"A man was assaulted at this intersection because the street light has been out for months."* This text describes real violence but is a legitimate safety concern. Should the system block it, flag it for human review, or pass it through? What factors would you weigh in making that decision?

You should not block it because it's a real safety hazard. Blocking it means it doesn't get reported and that defeats the purpose of a 311 system. So yes, flag it for human review. 