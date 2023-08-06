from alphabet_std import alphabet_std
from lookalikes import lookalikes
from prevent_misreadings import prevent_misreadings

human_alphabet = prevent_misreadings(alphabet_std, lookalikes)

if __name__ == '__main__':
    print(human_alphabet)
