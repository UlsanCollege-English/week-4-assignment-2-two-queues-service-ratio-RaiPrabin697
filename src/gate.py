from collections import deque

class Gate:
    def __init__(self):
        # Pattern is 1 fastpass, then 3 regulars
        self._pattern = ["fastpass", "regular", "regular", "regular"]
        self._idx = 0
        self._fast = deque()
        self._reg = deque()

    def arrive(self, line, person_id):
        if line == "fastpass":
            self._fast.append(person_id)
        elif line == "regular":
            self._reg.append(person_id)
        else:
            raise ValueError("Unknown line type")

    def serve(self):
        """
        Return the next person according to the repeating pattern.
        Skip empty lines but still move the cycle pointer correctly.
        Raise IndexError only if BOTH queues are empty.
        """
        # Nothing to serve at all
        if not self._fast and not self._reg:
            raise IndexError("Both lines are empty")

        # Try up to one full cycle
        for _ in range(len(self._pattern)):
            line_to_serve = self._pattern[self._idx]

            if line_to_serve == "fastpass" and self._fast:
                person = self._fast.popleft()
                self._idx = (self._idx + 1) % len(self._pattern)
                return person

            if line_to_serve == "regular" and self._reg:
                person = self._reg.popleft()
                self._idx = (self._idx + 1) % len(self._pattern)
                return person

            # Move pattern pointer and try again
            self._idx = (self._idx + 1) % len(self._pattern)

        # If we looped full cycle and found no one, then empty
        raise IndexError("Both lines are empty")

    def peek_next_line(self):
        """
        Predict which line will serve next without dequeuing anyone.
        """
        temp_idx = self._idx
        for _ in range(len(self._pattern)):
            line = self._pattern[temp_idx]
            if line == "fastpass" and self._fast:
                return "fastpass"
            if line == "regular" and self._reg:
                return "regular"
            temp_idx = (temp_idx + 1) % len(self._pattern)
        return None
