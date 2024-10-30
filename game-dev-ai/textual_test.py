from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Input
from textual.reactive import reactive


class CountdownTimer(Static):
    time_left = reactive(15, init=False)  # Set initial countdown time in seconds

    def on_mount(self) -> None:
        self.tick_timer = self.set_interval(1, self.tick)  # Call tick every second

    def tick(self) -> None:
        self.time_left -= 1  # Decrease the countdown by 1 second
        if self.time_left < 0:  # Stop the timer when it reaches zero
            self.tick_timer.stop()

    def watch_time_left(self, time_left: int) -> None:
        time, seconds = divmod(time_left, 60)
        hours, minutes = divmod(time, 60)
        self.update(
            f"Time Left:\n\n{hours:02}:{minutes:02}:{seconds:02}"
        )  # Format time as HH:MM:SS


class InputOutputApp(App):
    CSS = """
    Horizontal {
        height: 100%;
    }
    #left-panel {
        width: 70%;
        height: 100%;
        border: solid green;
        padding: 1;
    }
    #right-panel {
        width: 30%;
        height: auto;
        border: solid green;
        padding: 1;
    }
    #input-area {
        margin: 1;
    }
    #output {
        height: 1fr;
        margin-top: 1;
        overflow-y: auto;
    }
    CountdownTimer {
        height: auto;
        min-height: 5;
        content-align: center middle;
        text-align: center;
        background: $boost;
    }
    """

    items_display = reactive(
        [[[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []]]
    )  # Nested list structure

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                Static("Items Display:", id="items-header"),
                Static(
                    "", id="items-list"
                ),  # This will display the nested list of items
                Input(id="input-area", placeholder="Type here and press Enter"),
                Static(id="output"),
                id="left-panel",
            ),
            CountdownTimer(id="right-panel"),  # Countdown timer on the right
        )

    def on_mount(self) -> None:
        self.query_one("#input-area").focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        input_widget = event.input
        self.add_item(input_widget.value)  # Add input value to the items_display
        self.update_items_list()  # Update the displayed list
        self.clear_output()  # Clear the previous output
        self.display_new_output(input_widget.value)  # Display the new value
        input_widget.value = ""

    def clear_output(self) -> None:
        output = self.query_one("#output", Static)
        output.update("")  # Clear the output display

    def display_new_output(self, new_value: str) -> None:
        output = self.query_one("#output", Static)
        output.update(f"You entered: {new_value}")  # Display the new value

    def add_item(self, item: str) -> None:
        # Logic to add the item to the nested list structure
        for i in range(len(self.items_display)):
            for j in range(len(self.items_display[i])):
                if len(self.items_display[i][j]) < 4:  # Limit each sub-list to 4 items
                    self.items_display[i][j].append(item)
                    return

    def update_items_list(self) -> None:
        # Update the items list displayed in the UI
        items_display_str = ""
        for row in self.items_display:
            for sublist in row:
                items_display_str += " | ".join(sublist) + "\n"
            items_display_str += "\n"
        self.query_one("#items-list").update(items_display_str.strip())


if __name__ == "__main__":
    app = InputOutputApp()
    app.run()
