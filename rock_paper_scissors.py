import random

def get_computer_choice():
    """Return a random choice for the computer."""
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(human_choice, computer_choice):
    """
    Determine the winner of a single round.
    Returns 1 if human wins, -1 if computer wins, 0 if tie.
    """
    if human_choice == computer_choice:
        return 0

    if human_choice == 'rock':
        return 1 if computer_choice == 'scissors' else -1
    elif human_choice == 'paper':
        return 1 if computer_choice == 'rock' else -1
    elif human_choice == 'scissors':
        return 1 if computer_choice == 'paper' else -1

def play_round(human_choice, computer_choice):
    """Play a single round and display the result."""
    result = determine_winner(human_choice, computer_choice)

    print(f"\nYou chose: {human_choice}")
    print(f"Computer chose: {computer_choice}")

    if result == 0:
        print("It's a tie!")
    elif result == 1:
        print("You win this round!")
    else:
        print("Computer wins this round!")

    return result

def main():
    """Main game loop."""
    print("=" * 50)
    print("Welcome to Rock Paper Scissors!")
    print("First to win 5 games wins the match!")
    print("=" * 50)

    human_wins = 0
    computer_wins = 0

    while human_wins < 5 and computer_wins < 5:
        print(f"\n--- Score: You {human_wins} | Computer {computer_wins} ---")

        valid_choices = ['rock', 'paper', 'scissors']
        human_choice = None

        while human_choice not in valid_choices:
            human_choice = input("\nEnter your choice (rock/paper/scissors): ").lower().strip()
            if human_choice not in valid_choices:
                print("Invalid choice! Please enter rock, paper, or scissors.")

        computer_choice = get_computer_choice()
        result = play_round(human_choice, computer_choice)

        if result == 1:
            human_wins += 1
        elif result == -1:
            computer_wins += 1

    print("\n" + "=" * 50)
    print("GAME OVER!")
    print(f"Final Score: You {human_wins} | Computer {computer_wins}")

    if human_wins == 5:
        print("🎉 Congratulations! You won the match!")
    else:
        print("💻 Computer wins the match! Better luck next time!")
    print("=" * 50)

if __name__ == "__main__":
    main()
