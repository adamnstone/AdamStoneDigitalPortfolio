using System;
using System.Collections.Generic;

namespace SudokuSolver
{
    struct Num
    {
        public int num;
    }
    struct Pos
    {
        public int x;
        public int y;
    }
    struct FullMove
    {
        public Pos pos;
        public int move;
        public bool isNothing;
    }
    class Program
    {
        static int squareSize;

        static void Main(string[] args)
        {
            int dim;
            Num[,] board = CollectData(out dim);

            SolveBoard(board, dim);

            Console.WriteLine("No More Solutions!");
            Console.WriteLine();
            Console.WriteLine();
            Console.Write("Click Enter To Exit: ");
            Console.Write("Click Enter To Exit: ");
            Console.ReadLine();
        }

        static void SolveBoard(Num[,] board_, int dim, int depth = 1)
        {
            Num[,] board = board_;
            for (int y = 0; y < dim; y++)
            {
                for (int x = 0; x < dim; x++)
                {
                    int space = GetFromBoard(board, x, y).num;
                    if (space == 0)
                    {
                        for (int move = 1; move < dim + 1; move++)
                        {
                            if (IsMovePossible(board, x, y, move, dim))
                            {
                                MakeMove(board, x, y, move, out board);
                                SolveBoard(board, dim, depth: depth + 1);
                                UnMakeMove(board, x, y, out board);
                            }
                        }
                        return;
                    }
                }
            }
            Console.WriteLine("FINAL SOLUTION: ");
            DisplayBoard(board, dim);
            Console.WriteLine();
            Console.Write("To Find Another Solution, Click Enter: ");
            Console.ReadLine();
            Console.WriteLine();
            Console.WriteLine();
        }

        static bool HasSpaces(Num[,] board, int dim)
        {
            for (int y = 0; y < dim; y++)
            {
                for (int x = 0; x < dim; x++)
                {
                    if (GetFromBoard(board, x, y).num == 0)
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        static void MakeMove(Num[,] board__, int x, int y, int move, out Num[,] board_)
        {
            Num[,] board = board__;
            if (board[y, x].num != 0)
            {
                Console.WriteLine("MOVING ON TOP OF MOVE");
            }
            board[y, x] = new Num();
            board[y, x].num = move;
            board_ = board;
        }

        static void UnMakeMove(Num[,] board__, int x, int y, out Num[,] board_)
        {
            Num[,] board = board__;
            board[y, x].num = 0;
            board_ = board;
        }

        static bool IsMovePossible(Num[,] board, int x, int y, int move, int dim)
        {
            for (int p = 0; p < dim; p++)
            {
                if (p != x)
                {
                    if (GetFromBoard(board, p, y).num == move)
                    {
                        return false;
                    }
                }
                if (p != y)
                {
                    if (GetFromBoard(board, x, p).num == move)
                    {
                        return false;
                    }
                }
            }
            int xSquare = RoundDown((float)x / squareSize);
            int ySquare = RoundDown((float)y / squareSize);
            List<int> numbersSeen = new List<int>();
            for (int x_ = 0; x_ < squareSize; x_++)
            {
                for (int y_ = 0; y_ < squareSize; y_++)
                {
                    int space = GetFromBoard(board, (xSquare * squareSize) + x_, (ySquare * squareSize) + y_).num;
                    if (space == 0)
                    {
                        continue;
                    }
                    if (Includes(numbersSeen, space))
                    {
                        return false;
                    }
                    else
                    {
                        numbersSeen.Add(space);
                    }
                }
            }
            return true;
        }

        static int RoundDown(float n)
        {
            int i = (int)n;
            if (i > n)
            {
                return i - 1;
            }
            else
            {
                return i;
            }
        }

        static bool Includes(List<int> l, int i)
        {
            foreach (int j in l)
            {
                if (i == j)
                {
                    return true;
                }
            }
            return false;
        }

        static void DisplayBoard(Num[,] board, int dim)
        {
            for (int y = 0; y < dim; y++)
            {
                for (int x = 0; x < dim; x++)
                {
                    if (x != dim - 1)
                    {
                        Console.Write(board[y, x].num + ", ");
                    }
                    else
                    {
                        Console.WriteLine(board[y, x].num);
                    }
                }
            }
        }

        static Num[,] CollectData(out int dim_)
        {
            Console.Write("Width: ");
            int dim = int.Parse(Console.ReadLine());
            Console.Write("Small Square Size: ");
            squareSize = int.Parse(Console.ReadLine());
            dim_ = dim;
            Num[,] board = new Num[dim, dim];
            for (int i = 0; i < dim; i++)
            {
                Console.Write("Enter Line " + (i + 1) + " Separated By Commas With X for Blank: ");
                string line = Console.ReadLine();
                string[] lineSplitUp = line.Split(",");
                for (int j = 0; j < lineSplitUp.Length; j++)
                {
                    board[i, j] = new Num();
                    try
                    {
                        board[i, j].num = int.Parse(lineSplitUp[j]);
                    }
                    catch
                    {
                        board[i, j].num = 0;
                    }
                }
            }
            return board;
        }

        static Num GetFromBoard(Num[,] board, int x, int y)
        {
            return board[y, x];
        }
    }
}
