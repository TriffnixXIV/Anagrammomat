import tkinter as tk
from tkinter.font import Font

from anagram_generator import *

class Anagrammomat(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Anagrammomat")
        self.anagram_generator = AnagramGenerator()

        large_font = Font(family="Latin Modern Mono Caps", size=32)
        medium_font = Font(family="Latin Modern Mono Caps", size=24)
        small_font = Font(family="Latin Modern Mono Caps", size=16)

        self.source = tk.StringVar(value="Input")
        self.source.trace("w", self.update_output)

        core_frame = tk.Frame(self, bg="#4040C0")
        core_frame.grid(row=0, column=0)

        tk.Label(core_frame, bg="#4040C0", fg="#F0F0C0", text="ANAGRAMMOMAT", font=large_font).grid(row=0, column=0, padx=20, pady=20)

        tk.Entry(core_frame, bg="#F0F0C0", fg="#3030B0", textvariable=self.source, width=50, font=small_font, justify="center").grid(row=1, column=0, padx=20, pady=20)

        output_frame = tk.Frame(core_frame, bg="#3030B0", borderwidth=3, relief="solid")
        output_frame.grid(row=2, column=0, padx=20, pady=20)

        self.output_variables = [tk.StringVar(value="") for _ in range(5)]
        self.output_labels = [tk.Label(output_frame, bg="#3030B0", fg="#F0F0C0", font=medium_font, textvariable=outvar) for outvar in self.output_variables]

        for row in range(5):
            self.output_labels[row].grid(row=row, column=0, padx=20)

            if row == 0:
                self.output_labels[row].grid_configure(pady=(10, 0))
            elif row == 4:
                self.output_labels[row].grid_configure(pady=(0, 10))
            
            self.output_labels[row].bind("<Button-1>", lambda _, row=row: self.copy_to_clipboard(row))
            self.output_labels[row].bind("<Button-3>", lambda _, row=row: self.reroll_output(row))
            self.output_labels[row].bind("<Enter>", lambda _, row=row: self.output_labels[row].configure(bg="#4040C0"))
            self.output_labels[row].bind("<Leave>", lambda _, row=row: self.output_labels[row].configure(bg="#3030B0"))
        
        tk.Button(core_frame, bg="#F0F0C0", fg="#3030B0", text="Retry", font=small_font, command=self.update_output).grid(row=3, column=0, padx=20, pady=20)

        self.forced_word = tk.StringVar(value="")
        self.forced_word.trace("w", self.update_output)

        self.forced_word_entry = tk.Entry(core_frame, bg="#F0F0C0", fg="#3030B0", textvariable=self.forced_word, width=25, font=small_font, justify="center")
        self.forced_word_entry.grid(row=4, column=0, padx=20, pady=(20, 0))

        tk.Label(core_frame, bg="#4040C0", fg="#F0F0C0", text="forced word", font=small_font).grid(row=5, column=0, padx=20, pady=(0, 20))

        self.update_output()

    def update_output(self, *_):
        source = self.source.get()
        if len(source) > 4:
            source_histogram = generate_histogram(source)
            forced_word = self.forced_word.get()
            
            if can_histogram_accomodate_string(source_histogram, forced_word):
                self.forced_word_entry.configure(bg="#F0F0C0")
                self.anagram_generator.set_histogram(source_histogram)
                for i in range(5):
                    try:
                        anagram = self.anagram_generator.generate_anagram()
                        self.output_variables[i].set(f"{forced_word} {anagram}")
                    except Exception:
                        self.output_variables[i].set("???")
            else:
                self.forced_word_entry.configure(bg="#F0A0A0")
                for outvar in self.output_variables:
                    outvar.set(" - ")
        else:
            for outvar in self.output_variables:
                outvar.set(" - ")
    
    def reroll_output(self, row: int):
        try:
            anagram = self.anagram_generator.generate_anagram()
            self.output_variables[row].set(anagram)
        except Exception:
            self.output_variables[row].set("???")
    
    def copy_to_clipboard(self, row: int):
        self.clipboard_clear()
        self.clipboard_append(self.output_variables[row].get())

def can_histogram_accomodate_string(histogram: dict[str, int], string: str):
    """Returns whether the string can be built from the letters in the histogram.
    Modifies the given histogram to count down the letters."""
    if string != "":
        forced_word_histogram = generate_histogram(string)
        for letter, amount in forced_word_histogram.items():
            if letter in "abcdefghijklmnopqrstuvwxyz":
                if letter in histogram.keys() and histogram[letter] >= amount:
                    histogram[letter] -= amount
                else:
                    return False
    return True

def main():
    root = Anagrammomat()
    root.mainloop()

if __name__ == "__main__":
    main()