using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public Board mBoard;

    public PieceManager mPieceManager;

    void Start()
    {
        // Create Board
        mBoard.Create();

        // Create Pieces
        mPieceManager.Setup(mBoard);
    }
}
