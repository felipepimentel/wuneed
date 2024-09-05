from textual.app import App
from textual.widgets import Header, Footer, Button, ScrollView
from rich.panel import Panel

class WuneedTUI(App):
    async def on_load(self) -> None:
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        self.body = ScrollView(Panel("Welcome to Wuneed TUI!"))
        await self.view.dock(self.body, edge="left", size=40)

        self.buttons = ScrollView()
        await self.buttons.mount(Button("Transcribe", variant="primary"))
        await self.buttons.mount(Button("Workflow", variant="primary"))
        await self.buttons.mount(Button("Assist", variant="primary"))
        await self.view.dock(self.buttons, edge="right", size=20)

tui = WuneedTUI()