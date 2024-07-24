<h1 align="center">Shifter</h1>
<h2 align="center">Transitioning utility designed for use with <a href="https://github.com/nnra6864/Ricer"/>Ricer</h2>

---

# Usage
I suggest using a shell script(example I provided is written in fish).
- Start Shifter and save it's PID:
```fish
python Path/To/Shifter.py > /dev/null 2>&1 &
set pid $last_pid
disown
```
- Start the transition by sending a signal to the Shifter:
```fish
kill -SIGUSR1 $pid
```
- I recommend using sleep with at least 0.1s between starting the Shifter and transition:
```fish
sleep 0.1
```

---

# [Showcase](https://youtu.be/3OWSWnBabnE)
# [Example](https://github.com/nnra6864/Hyprnord/blob/9c0fbf471245abc74bdec300c0f9aaaf37eb4ee9/fish/config.fish#L13)
