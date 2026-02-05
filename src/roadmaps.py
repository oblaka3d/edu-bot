"""Roadmap parser — parse markdown roadmaps into structured data."""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

ROADMAPS_DIR = Path(__file__).parent.parent / "roadmaps"


@dataclass
class Topic:
    stage: int
    stage_name: str
    topic_num: int
    title: str
    content: List[str]
    practice: List[str]
    resources: List[Dict[str, str]]
    videos: List[Dict[str, str]]


@dataclass
class Stage:
    number: int
    name: str
    duration: str
    topics: List[Topic]


@dataclass
class Roadmap:
    track: str
    title: str
    description: str
    stages: List[Stage]
    total_topics: int


def parse_roadmap(track: str) -> Optional[Roadmap]:
    """Parse markdown roadmap file."""
    file_path = ROADMAPS_DIR / f"{track}.md"
    
    if not file_path.exists():
        return None
    
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    
    # Parse header
    title_match = re.search(r"# (.+)", content)
    title = title_match.group(1) if title_match else track
    
    # Parse description (can be multiline after >)
    desc_lines = []
    in_desc = False
    for line in lines:
        if line.startswith("> "):
            desc_lines.append(line[2:])
            in_desc = True
        elif in_desc and line.strip() and not line.startswith("#"):
            desc_lines.append(line)
        elif in_desc and (line.startswith("#") or line.startswith("---")):
            break
    description = " ".join(desc_lines) if desc_lines else ""
    
    stages = []
    current_stage = None
    current_topic = None
    total_topics = 0
    
    section = None
    
    for line in lines:
        line = line.strip()
        
        # Stage header: ## Этап 1: Name
        stage_match = re.match(r"##\s+Этап\s+(\d+):\s+(.+)", line)
        if stage_match:
            if current_topic and current_stage:
                current_stage.topics.append(current_topic)
            if current_stage:
                stages.append(current_stage)
            
            stage_num = int(stage_match.group(1))
            stage_name = stage_match.group(2)
            current_stage = Stage(number=stage_num, name=stage_name, duration="", topics=[])
            current_topic = None
            continue
        
        # Duration: **Длительность:** X weeks
        if "**Длительность:**" in line and current_stage:
            duration_match = re.search(r"\*\*Длительность:\*\*\s*(.+)", line)
            if duration_match:
                current_stage.duration = duration_match.group(1)
            continue
        
        # Topic header: ### Тема X.Y: Title
        topic_match = re.match(r"###\s+Тема\s+(\d+)\.(\d+):\s+(.+)", line)
        if topic_match:
            if current_topic and current_stage:
                current_stage.topics.append(current_topic)
            
            stage_num = int(topic_match.group(1))
            topic_num = int(topic_match.group(2))
            topic_title = topic_match.group(3)
            
            current_topic = Topic(
                stage=stage_num,
                stage_name=current_stage.name if current_stage else "",
                topic_num=topic_num,
                title=topic_title,
                content=[],
                practice=[],
                resources=[],
                videos=[]
            )
            total_topics += 1
            section = "content"
            continue
        
        # Section headers (with or without emoji)
        if line in ["**Практика:**", "💻 **Практика:**"]:
            section = "practice"
            continue
        elif line in ["**Ресурсы:**", "📚 **Ресурсы:**"]:
            section = "resources"
            continue
        elif line in ["**Видео:**", "🎥 **Видео:**"]:
            section = "videos"
            continue
        elif line in ["**Изучим:**", "📖 **Изучим:**"]:
            section = "content"
            continue
        elif line.startswith("---"):
            section = None
            continue
        
        # Parse content based on section
        if not line or not current_topic:
            continue
        
        # Support both "- " and "• " list markers
        list_marker = None
        if line.startswith("- "):
            list_marker = "- "
        elif line.startswith("• "):
            list_marker = "• "
        
        if list_marker:
            content_text = line[len(list_marker):]
            
            if section == "content":
                current_topic.content.append(content_text)
            elif section == "practice":
                current_topic.practice.append(content_text)
            elif section == "resources":
                # Parse markdown link: [text](url)
                link_match = re.search(r"\[(.+?)\]\((.+?)\)", content_text)
                if link_match:
                    current_topic.resources.append({
                        "title": link_match.group(1),
                        "url": link_match.group(2)
                    })
                else:
                    current_topic.resources.append({"title": content_text, "url": ""})
            elif section == "videos":
                link_match = re.search(r"\[(.+?)\]\((.+?)\)", content_text)
                if link_match:
                    current_topic.videos.append({
                        "title": link_match.group(1),
                        "url": link_match.group(2)
                    })
    
    # Add last topic and stage
    if current_topic and current_stage:
        current_stage.topics.append(current_topic)
    if current_stage:
        stages.append(current_stage)
    
    return Roadmap(
        track=track,
        title=title,
        description=description,
        stages=stages,
        total_topics=total_topics
    )


def get_all_tracks() -> List[str]:
    """Get list of available tracks."""
    tracks = []
    for file in ROADMAPS_DIR.glob("*.md"):
        tracks.append(file.stem)
    return tracks


def format_topic_for_display(topic: Topic, total_in_stage: int) -> str:
    """Format topic for Telegram message."""
    lines = [
        f"🎓 **{topic.title}**",
        f"",
        f"📚 *Этап {topic.stage}: {topic.stage_name}*",
        f"Тема {topic.topic_num} из {total_in_stage}",
        f""
    ]
    
    # Videos first for Telegram preview
    if topic.videos:
        lines.append("🎥 *Видео:*")
        for video in topic.videos:
            lines.append(f"• [{video['title']}]({video['url']})")
        lines.append("")
    
    if topic.content:
        lines.append("📖 *Изучим:*")
        for item in topic.content:
            lines.append(f"• {item}")
        lines.append("")
    
    if topic.resources:
        lines.append("📚 *Ресурсы:*")
        for res in topic.resources:
            if res['url']:
                lines.append(f"• [{res['title']}]({res['url']})")
            else:
                lines.append(f"• {res['title']}")
        lines.append("")
    
    if topic.practice:
        lines.append("💻 *Практика:*")
        for item in topic.practice:
            lines.append(f"• {item}")
        lines.append("")
    
    return "\n".join(lines)


def get_track_display_name(track: str) -> str:
    """Get human-readable track name."""
    mapping = {
        "go-backend": "🚀 Go Backend",
        "python-backend": "🐍 Python Backend",
        "js-frontend": "⚡ JavaScript Frontend"
    }
    return mapping.get(track, track)
