from langchain.prompts import PromptTemplate

class MeetingPromptTemplates:
    """Collection of prompt templates for meeting summarization"""
    
    @staticmethod
    def get_executive_summary_prompt():
        """Template for executive summary"""
        template = """
You are an expert meeting analyst. Create a comprehensive executive summary of the following meeting transcript.

MEETING TRANSCRIPT:
{transcript}

Please provide a structured summary with the following sections:

## Executive Summary
Provide a 2-3 sentence high-level overview of the meeting's purpose and outcomes.

## Key Discussion Points
- List the main topics discussed (3-5 bullet points)
- Include important details and context for each point

## Decisions Made
- List all decisions that were finalized during the meeting
- Include who made the decision and any conditions

## Action Items
- List specific tasks assigned with responsible parties
- Include deadlines if mentioned
- Format: [Person] - [Task] - [Deadline if available]

## Next Steps
- Outline what happens next
- Include any follow-up meetings or milestones

## Participants & Roles
- Identify key participants and their roles (if discernible from transcript)

Keep the summary professional, concise, and actionable. Focus on concrete outcomes rather than discussion process.
"""
        return PromptTemplate(
            input_variables=["transcript"],
            template=template
        )
    
    @staticmethod
    def get_topic_extraction_prompt():
        """Template for extracting key topics"""
        template = """
Analyze the following meeting transcript and extract the key topics discussed.

TRANSCRIPT:
{transcript}

Please identify:
1. Main topics (3-5 primary subjects)
2. Subtopics under each main topic
3. The relative importance of each topic (High/Medium/Low)
4. Any recurring themes or patterns

Format your response as a structured list with clear categorization.
"""
        return PromptTemplate(
            input_variables=["transcript"],
            template=template
        )
    
    @staticmethod
    def get_action_items_prompt():
        """Template for extracting action items"""
        template = """
Extract all action items, tasks, and commitments from the following meeting transcript.

TRANSCRIPT:
{transcript}

For each action item, identify:
- The specific task or action
- Who is responsible (if mentioned)
- Deadline or timeline (if mentioned)
- Priority level (if discernible)
- Dependencies (if any)

Format as a clear, actionable list. If information is not explicitly stated, mark as "Not specified".
"""
        return PromptTemplate(
            input_variables=["transcript"],
            template=template
        )
    
    @staticmethod
    def get_sentiment_analysis_prompt():
        """Template for sentiment and tone analysis"""
        template = """
Analyze the sentiment and tone of the following meeting transcript.

TRANSCRIPT:
{transcript}

Provide analysis on:
1. Overall meeting tone (Professional, Collaborative, Tense, etc.)
2. Key sentiment indicators
3. Areas of agreement vs. disagreement
4. Engagement level of participants
5. Any concerns or issues raised

Keep the analysis objective and professional.
"""
        return PromptTemplate(
            input_variables=["transcript"],
            template=template
        )
    
    @staticmethod
    def get_comprehensive_summary_prompt():
        """Template for comprehensive multi-section summary"""
        template = """
You are an expert meeting analyst. Analyze the following meeting transcript and create a comprehensive, structured summary.

MEETING TRANSCRIPT:
{transcript}

Create a detailed summary with these sections:

# Meeting Summary Report

## 📋 Executive Summary
Provide a concise 2-3 sentence overview of the meeting's main purpose and key outcomes.

## 🎯 Key Discussion Points
List the main topics discussed with brief context:
- Topic 1: [Brief description]
- Topic 2: [Brief description]
- Topic 3: [Brief description]

## ✅ Decisions Made
Document all decisions reached during the meeting:
- Decision 1: [What was decided and by whom]
- Decision 2: [What was decided and by whom]

## 📝 Action Items
List all tasks and assignments:
- [ ] [Task description] - Assigned to: [Person] - Due: [Date/Timeline]
- [ ] [Task description] - Assigned to: [Person] - Due: [Date/Timeline]

## 🔄 Next Steps
Outline immediate next steps and follow-up actions:
- [Next step 1]
- [Next step 2]

## 👥 Participants
List key participants and their roles (if identifiable):
- [Name/Role]: [Brief contribution or role in meeting]

## 📊 Meeting Metrics
- Duration: [If mentioned or estimable]
- Main Focus: [Primary meeting objective]
- Outcome: [Success/Needs follow-up/Inconclusive]

## 🚨 Important Notes
Highlight any critical information, concerns, or urgent items that require immediate attention.

Format the response in clean markdown. Be specific and actionable. If information is not available in the transcript, note it as "Not specified" rather than making assumptions.
"""
        return PromptTemplate(
            input_variables=["transcript"],
            template=template
        )
