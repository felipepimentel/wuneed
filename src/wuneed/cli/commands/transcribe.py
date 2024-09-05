import typer
from rich import print
from wuneed.integrations import transcription

app = typer.Typer()

@app.command()
def video(
    source: str = typer.Argument(..., help="URL or path to the video file"),
    output: str = typer.Option("transcript.txt", help="Output file for the transcript")
):
    """Transcribe audio from a video file or URL."""
    try:
        transcript = transcription.transcribe_video(source)
        with open(output, "w") as f:
            f.write(transcript)
        print(f"[green]Transcription completed. Output saved to {output}[/green]")
    except Exception as e:
        print(f"[red]Error during transcription: {str(e)}[/red]")