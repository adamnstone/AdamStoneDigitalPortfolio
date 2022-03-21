using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

public class Pawn : BasePiece
{

    public override void Setup(Color newTeamColor, Color newSpriteColor, PieceManager newPieceManager)
    {
        // Base Setup
        base.Setup(newTeamColor, newSpriteColor, newPieceManager);

        // Reset
        mIsFirstMove = true;

        // Pawn Stuff
        mMovement = mColor == Color.white ? new Vector3Int(0, 1, 1) : new Vector3Int(0, -1, -1);
        GetComponent<Image>().sprite = Resources.Load<Sprite>("T_Pawn");
    }

    private bool MatchesState(int targetX, int targetY, CellState targetState)
    {
        CellState cellState = mCurrentCell.mBoard.ValidateCell(targetX, targetY, this);
        Debug.Log(targetX + ", " + targetY + " is " + cellState + " and checking for " + targetState);
        if (cellState == targetState)
        {
            mHighlightedCells.Add(mCurrentCell.mBoard.mAllCells[targetX, targetY]);
            return true;
        }
        return false;
    }

    public override void Reset()
    {
        base.Reset();
        mIsFirstMove = true;
    }

    public override void CheckPathing(bool human = false)
    {
        // Clear Pathing
        ClearCells();

        // Target Position
        int currentX = mCurrentCell.mBoardPosition.x;
        int currentY = mCurrentCell.mBoardPosition.y;

        // Forward
        if (MatchesState(currentX, currentY + mMovement.y, CellState.Free))
        {
            // If Is First Move And Cell One Ahead Is Free Check Next
            if ((mIsWhite && mCurrentCell.mBoardPosition.y == 1) || (!mIsWhite && mCurrentCell.mBoardPosition.y == 6))
            {
                MatchesState(currentX, currentY + (mMovement.y * 2), CellState.Free);
            }
        }

        // Top Right
        MatchesState(currentX + mMovement.z, currentY + mMovement.z, CellState.Enemy);

        // Top Left
        MatchesState(currentX - mMovement.z, currentY + mMovement.z, CellState.Enemy);
    }
}
