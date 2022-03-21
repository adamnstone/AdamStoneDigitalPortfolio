using System;
using System.Collections.Generic;
using UnityEngine;

public class PieceManager : MonoBehaviour
{
    [HideInInspector]
    public bool mIsKingAlive = true;
    public GameObject mPiecePrefab;

    public Color mWhiteTeamColor = Color.white;
    public Color mBlackTeamColor = Color.black;

    public Transform cellHolder;

    [Header("AI Settings")]
    public bool vsAI = true;
    public bool isAIWhite = false;
    [Header("Examples")]
    public int mTestPositionNumber = 0;
    [Header("Optimization")]
    public bool mUseAlphaBetaPruning = false;
    [Header("Player Settings")]
    public bool mEnsureHumanMovesAreValid = true;
    [Header("Graphics Settings")]
    public float mComputerMovementLeeway = 0.1f;
    public float mPieceSpeed = 1f;
    [Header("AI Hyperparameters")]
    public float mKingNearEdgeImportance = 1f;
    public int depth = 3;
    [Tooltip("Not Counting Pawns")]
    public int mDepthAddOneThreshold = 6;
    [Tooltip("Not Counting Pawns")]
    public int mCheckNextBestThreshold = 6;
    [Tooltip("Not Counting Pawns")]
    public int mMoveKingAwayFromSidesThreshold = 6;
    public float pawnWorth = 1;
    public float rookWorth = 5;
    public float knightWorth = 3;
    public float bishopWorth = 3;
    public float queenWorth = 9;

    private float pawnCountWhite = 8;//DO NOT CHANGE AUTOMATICALLY NEED TO ManuALLY! for PAWN CHESS
    private float rookCountWhite = 2;
    private float knightCountWhite = 2;
    private float bishopCountWhite = 2;
    private float queenCountWhite = 1;

    private float pawnCount = 16;//DO NOT CHANGE AUTOMATICALLY NEED TO ManuALLY! for PAWN CHESS
    private float rookCount = 4;
    private float knightCount = 4;
    private float bishopCount = 4;
    private float queenCount = 2;

    public float mForwardImportance = 1f;
    public float mSquareTableImportance = 1f;

    private int positionsSearched = 0;
    [HideInInspector]
    public int mTotalPieceCount;
    [HideInInspector]
    public int mRoyaltyCount;

    [HideInInspector]
    public Vector2Int mWhiteKingPosition;
    [HideInInspector]
    public Vector2Int mBlackKingPosition;

    private List<BasePiece> mWhitePieces = null;
    private List<BasePiece> mBlackPieces = null;

    [HideInInspector]
    public bool mGameIsOver = false;

    private Board mBoard;

    private StoreStringAndPos[][][] mOpeningBookBlack = new StoreStringAndPos[][][]
    {
        new StoreStringAndPos[][]
        {
            new StoreStringAndPos[]
            {
                new StoreStringAndPos("KN", 5, 5, b_: false),
                new StoreStringAndPos("KN", 5, 7, b_: false)
            }
        }
    };

    private string[] mPieceOrderWhite = new string[16]
    {
       "P", "P", "P", "P", "P", "P", "P", "P",
       "R", "KN", "B", "Q", "K", "B", "KN", "R"
    };

    private string[] mPieceOrderBlack = new string[16]
    {
        "P", "P", "P", "P", "P", "P", "P", "P",
        "R", "KN", "B", "Q", "K", "B", "KN", "R"
    };

    private Dictionary<string, Type> mPieceLibrary = new Dictionary<string, Type>()
    {
        {"P", typeof(Pawn)},
        {"R", typeof(Rook)},
        {"KN", typeof(Knight)},
        {"B", typeof(Bishop)},
        {"K", typeof(King)},
        {"Q", typeof(Queen)}
    };

    public Dictionary<string, float> mWhiteCountLibrary;
    public Dictionary<string, float> mCountLibrary;
    public Dictionary<string, int[][]> mSquareTableLibrary;
    private string[] mScorePieces = new string[5]
    {
        "P", "R", "KN", "B", "Q"
    };

    private Dictionary<string, float> mWorthLibrary;
    
    private int GetAmountOfRoyaltyInInitialization()
    {
        int count = 0;
        foreach (string s in mPieceOrderWhite)
        {
            if (s != "P" && s != "")
            {
                count++;
            }
        }
        foreach (string s in mPieceOrderBlack)
        {
            if (s != "P" && s != "")
            {
                count++;
            }
        }
        return count;
    }

    private int GetAmountOfPiecesInInitialization()
    {
        int count = 0;
        foreach (string s in mPieceOrderWhite)
        {
            if (s != "")
            {
                count++;
            }
        }
        foreach (string s in mPieceOrderBlack)
        {
            if (s != "")
            {
                count++;
            }
        }
        return count;
    }
    
    void Awake()
    {
        mTotalPieceCount = GetAmountOfPiecesInInitialization();
        mRoyaltyCount = GetAmountOfRoyaltyInInitialization();
        mWorthLibrary = new Dictionary<string, float>()
        {
            {"P", pawnWorth },
            {"R", rookWorth },
            {"KN", knightWorth },
            {"B", bishopWorth },
            {"Q", queenWorth },
        };
        mWhiteCountLibrary = new Dictionary<string, float>()
        {
            {"P", pawnCountWhite },
            {"R", rookCountWhite },
            {"KN", knightCountWhite },
            {"B", bishopCountWhite },
            {"Q", queenCountWhite },
        };
        mCountLibrary = new Dictionary<string, float>()
        {
            {"P", pawnCount },
            {"R", rookCount },
            {"KN", knightCount },
            {"B", bishopCount },
            {"Q", queenCount },
        };
        mSquareTableLibrary = new Dictionary<string, int[][]>()
        {
            {"P", PieceSquareTables.PawnSquareTables },
            {"R", PieceSquareTables.RookSquareTables },
            {"KN", PieceSquareTables.KnightSquareTables },
            {"B", PieceSquareTables.BishopSquareTables },
            {"Q", PieceSquareTables.QueenSquareTables },
        };
        if (mTestPositionNumber == 1)
        {
            mPieceOrderWhite = new string[16]
            {
                "", "", "", "", "", "", "", "",
                "", "", "", "", "K", "", "", ""
            };
            mPieceOrderBlack = new string[16]
            {
                "", "", "", "", "", "", "", "",
                "R", "", "", "", "K", "", "", "R"
            };
        }
    }

    public void Setup(Board board)
    {
        // Create Each Team's Pieces
        mWhitePieces = CreatePieces(Color.white, mWhiteTeamColor, board, mPieceOrderWhite);
        mBlackPieces = CreatePieces(Color.black, mBlackTeamColor, board, mPieceOrderBlack);

        // Place Pieces
        PlacePieces(1, 0, mWhitePieces, board);
        PlacePieces(6, 7, mBlackPieces, board);

        mBoard = board;

        SwitchSides(false);
    }

    private List<BasePiece> CreatePieces(Color teamColor, Color spriteColor, Board board, string[] pieceList)
    {
        List<BasePiece> newPieces = new List<BasePiece>();

        // Loop Through Starting Pieces Order
        for (int i = 0; i < pieceList.Length; i++)
        {
            // Create New Object
            GameObject newPieceObject = (GameObject)Instantiate(mPiecePrefab);
            newPieceObject.transform.SetParent(cellHolder);

            // Set Scale And Position
            newPieceObject.transform.localScale = Vector3.one;
            newPieceObject.transform.localRotation = Quaternion.identity;

            // Get The Type
            string key = pieceList[i];
            if (key == "")
            {
                newPieces.Add(null);
                Destroy(newPieceObject);
                continue;
            }
            Type pieceType = mPieceLibrary[key];

            // Store Piece
            BasePiece newPiece = (BasePiece)newPieceObject.AddComponent(pieceType);
            newPiece.mLetter = key;
            newPieces.Add(newPiece);

            // Setup Piece
            newPiece.Setup(teamColor, spriteColor, this);
        }

        return newPieces;
    }

    private void SetInteractive(List<BasePiece> allPieces, bool value)
    {
        foreach (BasePiece piece in allPieces)
            if (piece != null)
            {
                piece.enabled = value;
            }
    }

    public void SwitchSides(bool isWhite)
    {
        if (!mIsKingAlive)
        {
            // Reset Pieces
            //ResetPieces();

            // King Has Risen From The Dead
            mIsKingAlive = true;

            // Change Color To Black So White Can Go first Again
            isWhite = false;
        }

        // Set Interactivity
        SetInteractive(mWhitePieces, !isWhite);
        SetInteractive(mBlackPieces, isWhite);

        if (!isWhite == isAIWhite && vsAI)
        {
            Debug.Log("AI is Thinking");
            AITurn();
        }
    }

    public void ResetPieces()
    {
        // Reset White
        foreach (BasePiece piece in mWhitePieces)
            piece.Reset();

        // Reset Black
        foreach (BasePiece piece in mBlackPieces)
            piece.Reset();

        mGameIsOver = false;
    }

    private void PlacePieces(int pawnRow, int royaltyRow, List<BasePiece> pieces, Board board)
    {

        for (int i = 0; i < 8; i++)
        {
            // Place Pawns
            if (pieces[i] != null)
            {
                pieces[i].Place(board.mAllCells[i, pawnRow]);
            }

            // Place Royalty
            if (pieces[i + 8] != null)
            {
                pieces[i + 8].Place(board.mAllCells[i, royaltyRow]);
            }
        }
    }

    private double Evaluate()
    {
        double score = 0;
        for (int y = 0; y < 8; y++)
        {
            for (int x = 0; x < 8; x++)
            {
                BasePiece p = mBoard.mAllCells[x, y].mCurrentPiece;
                if (p == null)
                {
                    continue;
                }
                bool isKing = p.IsKing();
                bool isWhite = p.mIsWhite;


                // Piece Worth
                if (!isKing)
                {
                    score += (isWhite ? 1 : -1) * mWorthLibrary[p.mLetter];
                }

                // Other Factors
                if (!isKing)
                {
                    score += (p.mCurrentCell.mBoardPosition.y - 3.5) * mWorthLibrary[p.mLetter] * mForwardImportance;
                    score += (isWhite ? 1 : -1) * mSquareTableLibrary[p.mLetter][(isWhite ? 7 - y : y)][(isWhite ? x : 7 - x)] * mSquareTableImportance;
                }

                // If Game Is Over
                if (isKing && mGameIsOver)
                {
                    return isWhite ? double.PositiveInfinity : double.NegativeInfinity;
                }

                // King At Edge Near End
                if (mRoyaltyCount <= mMoveKingAwayFromSidesThreshold)
                {
                    int[] kingWhitePos = GetKingPosition(true);
                    int[] kingBlackPos = GetKingPosition(false);
                    int whiteDistance = (kingWhitePos[0] >= 4 ? (7 - kingWhitePos[0]) : (kingWhitePos[0])) + (kingWhitePos[1] >= 4 ? (7 - kingWhitePos[1]) : (kingWhitePos[1]));
                    int blackDistance = (kingBlackPos[0] >= 4 ? (7 - kingBlackPos[0]) : (kingBlackPos[0])) + (kingBlackPos[1] >= 4 ? (7 - kingBlackPos[1]) : (kingBlackPos[1]));
                    score += whiteDistance * mKingNearEdgeImportance;
                    score -= blackDistance * mKingNearEdgeImportance;
                }
            }
        }
        return score;
    }

    private double EvaluateDifferent()
    {
        double score = 0;
        foreach (string s in mScorePieces)
        {
            score += ((float)mCountLibrary[s] / 2 < mWhiteCountLibrary[s] ? mWhiteCountLibrary[s] * mWorthLibrary[s] : (mCountLibrary[s] - mWhiteCountLibrary[s]) * -1 * mWorthLibrary[s]);
        }
        return score;
    }

    private bool OpeningBookHasPosition()
    {
        return false;
    }

    private int GetBook(int[,] moves, int[,] originalPositions)

    {
        return -1;
    }

    private void AITurn()
    {
        int[,] moves;
        int[,] originalPositions;
        GetAllMoves(out moves, out originalPositions);
        positionsSearched = 0;
        int index;
        if (OpeningBookHasPosition())
        {
            index = GetBook(moves, originalPositions);
        }
        else
        {
            int depthToUse;
            if (mRoyaltyCount <= mDepthAddOneThreshold)
            {
                Debug.Log("Increase Depth Threshold Reached");
                depthToUse = depth + 1;
            }
            else
            {
                depthToUse = depth;
            }
            if (mRoyaltyCount <= mCheckNextBestThreshold)
            {
                Debug.Log("Check Next Best Threshold Reached");
            }
            if (mRoyaltyCount <= mMoveKingAwayFromSidesThreshold)
            {
                Debug.Log("Move King Away From Sides Threshold Reached");
            }
            StoreMoveAndScore minimax = Minimax(isAIWhite, depthToUse, double.NegativeInfinity, double.PositiveInfinity, moves_: moves, originalPositions_: originalPositions);
            index = minimax.move;
        }
        MakeMove(originalPositions[index, 0], originalPositions[index, 1], moves[index, 0], moves[index, 1], finalMove: true);
        SwitchSides(false);
        mBoard.ClearHighlighting();
        Debug.Log("Positions Searched: " + positionsSearched);
        Debug.Log("Decision: (" + originalPositions[index, 0] + ", " + originalPositions[index, 1] + "), (" + moves[index, 0] + ", " + moves[index, 1] + ")");
        Debug.Log("Decision Index: " + index);
        Debug.Log("Immediate Evaluation: " + Evaluate());
    }

    double Max(double d1, double d2)
    {
        return (d1 > d2 ? d1 : d2);
    }

    double Min(double d1, double d2)
    {
        return (d1 < d2 ? d1 : d2);
    }

    private StoreMoveAndScore Minimax(bool isMaximizing, int depth, double alpha_, double beta_, int[,] moves_ = null, int[,] originalPositions_ = null)// not making moves two deep
    {
        double alpha = alpha_;
        double beta = beta_;
        int[,] moves;
        int[,] originalPositions;
        GetAllMoves(out moves, out originalPositions, isUsingNonAI: true, optionalSide: isMaximizing);
        if (moves_ != null && originalPositions_ != null)
        {
            moves = moves_;
            originalPositions = originalPositions_;
        }
        if (mGameIsOver)
        {
            return new StoreMoveAndScore(-1, Evaluate());
        }
        else if (moves.Length == 0)
        {
            return new StoreMoveAndScore(-1, 0);
        }
        else if (mRoyaltyCount <= mCheckNextBestThreshold && depth == 0)
        {
            int[] kingPos = GetKingPosition(!isMaximizing);
            for (int i = 0; i < (float)moves.Length / 2; i++)
            {
                int x = moves[i, 0];
                int y = moves[i, 1];
                if (kingPos[0] == x && kingPos[1] == y)
                {
                    return new StoreMoveAndScore(-1, (isMaximizing ? double.PositiveInfinity : double.NegativeInfinity));
                }
            }
            return new StoreMoveAndScore(-1, Evaluate());
        }
        else if (depth == 0)
        {
            return new StoreMoveAndScore(-1, Evaluate());
        }
        
        double bestScore = isMaximizing ? double.NegativeInfinity : double.PositiveInfinity;
        int bestIndex = 0;
        int[] movesOrder = OrderMoves(originalPositions, moves);
        if (isMaximizing)
        {
            foreach (int i in movesOrder)
            {
                positionsSearched++;
                int x1 = originalPositions[i, 0];
                int y1 = originalPositions[i, 1];
                int x2 = moves[i, 0];
                int y2 = moves[i, 1];
                BasePiece p = MakeMove(x1, y1, x2, y2);
                double hypotheticalScore = Minimax(!isMaximizing, depth - 1, alpha, beta).score;
                MakeMove(x2, y2, x1, y1, pieceToGiveBack: p);
                if (hypotheticalScore > bestScore && !mUseAlphaBetaPruning)
                {
                    bestScore = hypotheticalScore;
                    bestIndex = i;
                }
                if (mUseAlphaBetaPruning)
                {
                    double oldAlpha = alpha;
                    alpha = Max(hypotheticalScore, alpha);
                    if (alpha != oldAlpha)
                    {
                        bestIndex = i;
                    }
                }
                if (alpha >= beta && mUseAlphaBetaPruning)
                {
                    return new StoreMoveAndScore(bestIndex, alpha);
                }
            }
        }
        else
        {
            foreach (int i in movesOrder)
            {
                positionsSearched++;
                int x1 = originalPositions[i, 0];
                int y1 = originalPositions[i, 1];
                int x2 = moves[i, 0];
                int y2 = moves[i, 1];
                BasePiece p = MakeMove(x1, y1, x2, y2);
                double hypotheticalScore = Minimax(!isMaximizing, depth - 1, alpha, beta).score;
                MakeMove(x2, y2, x1, y1, pieceToGiveBack: p);
                if (hypotheticalScore < bestScore && !mUseAlphaBetaPruning)
                {
                    bestScore = hypotheticalScore;
                    bestIndex = i;
                }
                if (mUseAlphaBetaPruning)
                {
                    double oldBeta = beta;
                    beta = Min(beta, hypotheticalScore);
                    if (beta != oldBeta)
                    {
                        bestIndex = i;
                    }
                }
                if (alpha >= beta && mUseAlphaBetaPruning)
                {
                    return new StoreMoveAndScore(bestIndex, beta);
                }
            }
        }
        if (!mUseAlphaBetaPruning)
        {
            if (depth == this.depth)
            {
                Debug.Log("Best Score: " + bestScore);
            }
            return new StoreMoveAndScore(bestIndex, bestScore);
        }
        else
        {
            if (depth == this.depth)
            {
                Debug.Log("Alpha: " + alpha);
                Debug.Log("Beta: " + beta);
            }
            if (isMaximizing)
            {
                return new StoreMoveAndScore(bestIndex, alpha);
            }
            else
            {
                return new StoreMoveAndScore(bestIndex, beta);
            }

        }
        
    }

    private int[] OrderMoves(int[,] originalPositions, int[,] moves)
    {
        float[] scores = new float[(int)(float)moves.Length / 2];
        for (int i = 0; i < (float)moves.Length / 2; i++)
        {
            BasePiece p = mBoard.mAllCells[moves[i, 0], moves[i, 1]].mCurrentPiece;
            if (p == null)
            {
                scores[i] = 0;
            }
            else if (!p.IsKing())
            {
                scores[i] = mWorthLibrary[p.mLetter] * (p.mIsWhite ? 1 : -1);
            }
        }
        int[] originalIndexes = new int[(int)(float)moves.Length / 2];
        for (int i = 0; i < originalIndexes.Length; i++)
        {
            originalIndexes[i] = i;
        }
        Array.Sort(scores, originalIndexes);
        originalIndexes = ReverseList(originalIndexes);
        return originalIndexes;
    }

    int[] ReverseList(int[] l)
    {
        List<int> newL = new List<int>();
        for (int i = l.Length - 1; i >= 0; i--)
        {
            newL.Add(l[i]);
        }
        return newL.ToArray();
    }

    float[] ReverseList(float[] l)
    {
        List<float> newL = new List<float>();
        for (int i = l.Length - 1; i >= 0; i--)
        {
            newL.Add(l[i]);
        }
        return newL.ToArray();
    }

    float[] CopyArray(float[] array)
    {
        float[] nArray = new float[array.Length];
        for (int i = 0; i < array.Length; i++)
        {
            nArray[i] = array[i];
        }
        return nArray;
    }


    private void GetAllMoves(out int[,] moves_, out int[,] originalPositions_, bool isUsingNonAI = false, bool optionalSide = true)
    {
        List<int[]> moves = new List<int[]>();
        List<int[]> originalPositions = new List<int[]>();
        List<BasePiece> piecesToGoThrough = isAIWhite ? mWhitePieces : mBlackPieces;
        if (isUsingNonAI)
        {
            piecesToGoThrough = optionalSide ? mWhitePieces : mBlackPieces;
        }
        foreach (BasePiece piece in piecesToGoThrough)
        {
            if (piece == null)
            {
                continue;
            }
            if (!piece.gameObject.activeSelf)
                continue;
            piece.CheckPathing();
            List<Cell> copy = CopyList(piece.mHighlightedCells);
            foreach (Cell cell in copy)
            {
                Vector2Int boardPosition = cell.mBoardPosition;
                moves.Add(new int[] { boardPosition.x, boardPosition.y });
                Vector2Int currentCellPosition = piece.mCurrentCell.mBoardPosition;
                originalPositions.Add(new int[] { currentCellPosition.x, currentCellPosition.y });
            }
        }
        moves_ = ConvertTo2DArray(moves);
        originalPositions_ = ConvertTo2DArray(originalPositions);
    }

    private int[,] ConvertTo2DArray(List<int[]> l)
    {
        if (l.Count == 0)
        {
            return new int[0, 0];
        }
        int[,] newL = new int[l.Count, l[0].Length];
        for (int i = 0; i < l.Count; i++)
        {
            for (int j = 0; j < l[i].Length; j++)
            {
                newL[i, j] = l[i][j];
            }
        }
        return newL;
    }

    private BasePiece MakeMove(int x1, int y1, int x2, int y2, BasePiece pieceToGiveBack = null, bool finalMove = false)
    {
        BasePiece takingAwayPiece = mBoard.mAllCells[x2, y2].mCurrentPiece;
        mBoard.mAllCells[x1, y1].mCurrentPiece.mTargetCell = mBoard.mAllCells[x2, y2];
        mBoard.mAllCells[x1, y1].mCurrentPiece.ClearCells();
        StartCoroutine(mBoard.mAllCells[x1, y1].mCurrentPiece.Move(delayedMovement: finalMove));

        if (pieceToGiveBack != null)
        {
            if (pieceToGiveBack.IsKing())
            {
                mGameIsOver = false;
            }
            mBoard.mAllCells[x1, y1].mCurrentPiece = pieceToGiveBack;
            mTotalPieceCount++;
            if (pieceToGiveBack.mLetter != "P")
            {
                mRoyaltyCount++;
            }
            if (pieceToGiveBack.mShouldRestoreFirstMove)
            {
                mBoard.mAllCells[x1, y1].mCurrentPiece.mIsFirstMove = true;
            }
            pieceToGiveBack.gameObject.SetActive(true);
        }
        else
        {
            return takingAwayPiece;
        }
        return null;
    }

    private int[] GetKingPosition(bool isWhite)
    {
        for (int y = 0; y < 8; y++)
        {
            for (int x = 0; x < 8; x++)
            {
                BasePiece piece = mBoard.mAllCells[x, y].mCurrentPiece;
                if (piece == null)
                {
                    continue;
                }
                if (piece.IsKing() && piece.mIsWhite == isWhite)
                {
                    return new int[2] { x, y };
                }
            }
        }
        return new int[2] { -1, -1 };
    }

    private List<Cell> CopyList(List<Cell> l)
    {
        List<Cell> newL = new List<Cell>();
        foreach (Cell c in l)
        {
            newL.Add(c);
        }
        return newL;
    }


    public bool ValidateMove(BasePiece piece, int targetX, int targetY)
    {
        if (!mEnsureHumanMovesAreValid)
        {
            return true;
        }
        int x1 = piece.mCurrentCell.mBoardPosition.x;
        int y1 = piece.mCurrentCell.mBoardPosition.y;
        int x2 = targetX;
        int y2 = targetY;
        Cell originalTargetCell = piece.mTargetCell; 
        BasePiece pieceToGiveBack = MakeMove(x1, y1, x2, y2);
        int[,] moves;
        int[,] originalPositions;
        GetAllMoves(out moves, out originalPositions, isUsingNonAI: true, optionalSide: !piece.mIsWhite);
        int[] oppositeKingPosition = GetKingPosition(piece.mIsWhite);//moe in loop if no work?
        for (int i = 0; i < (float)moves.Length / 2; i++)
        {
            if ((moves[i, 0] == oppositeKingPosition[0] && moves[i, 1] == oppositeKingPosition[1]))
            {
                MakeMove(x2, y2, x1, y1, pieceToGiveBack: pieceToGiveBack);
                piece.mTargetCell = originalTargetCell;
                
                return false;
            }
        }
        MakeMove(x2, y2, x1, y1, pieceToGiveBack: pieceToGiveBack);
        piece.mTargetCell = originalTargetCell;
        return true;
    }
}
