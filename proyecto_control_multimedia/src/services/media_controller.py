import subprocess


class MediaController:
    def execute(self, action: str) -> None:
        if action == "play_pause":
            self.play_pause()
        elif action == "next":
            self.next_track()
        elif action == "previous":
            self.previous_track()
        elif action == "volume_up":
            self.volume_up()
        elif action == "volume_down":
            self.volume_down()
        else:
            print(f"Acción no reconocida: {action}")

    def play_pause(self) -> None:
        self._run_command(["playerctl", "play-pause"])

    def next_track(self) -> None:
        self._run_command(["playerctl", "next"])

    def previous_track(self) -> None:
        self._run_command(["playerctl", "previous"])

    def volume_up(self) -> None:
        self._run_command(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+10%"])

    def volume_down(self) -> None:
        self._run_command(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-10%"])

    def _run_command(self, command: list[str]) -> None:
        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print(f"No se encontró el comando: {command[0]}")
        except subprocess.CalledProcessError:
            print(f"No se pudo ejecutar el comando: {' '.join(command)}")