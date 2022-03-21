using UnityEngine;
using UnityEngine.UI;

public class Knight : BasePiece
{
    public override void Setup(Color newTeamColor, Color newSpriteColor, PieceManager newPieceManager)
    {
        // Base Setup
        base.Setup(newTeamColor, newSpriteColor, newPieceManager);

        // Knight Stuff
        GetComponent<Image>().sprite = Resources.Load<Sprite>("T_Knight");
    }

    private void CreateCellPath(int flipper)
    {
        // Target Position
        int currentX = mCurrentCell.mBoardPosition.x;
        int currentY = mCurrentCell.mBoardPosition.y;

        // Left
        MatchesState(currentX - 2, currentY + (1 * flipper));

        // Upper Left
        MatchesState(currentX - 1, currentY + (2 * flipper));

        // Upper Right
        MatchesState(currentX + 1, currentY + (2 * flipper));

        // Right
        MatchesState(currentX + 2, currentY + (1 * flipper));
    }

    public override void CheckPathing(bool human = false)
    {
        // Clear Pathing
        ClearCells();

        // Draw Top Path
        CreateCellPath(1);

        // Draw Bottom Path
        CreateCellPath(-1);

    }

    private void MatchesState(int targetX, int targetY, bool r=false)
    {
        CellState cellState = mCurrentCell.mBoard.ValidateCell(targetX, targetY, this);

        if (cellState != CellState.Friendly && cellState != CellState.OutOfBounds)
            mHighlightedCells.Add(mCurrentCell.mBoard.mAllCells[targetX, targetY]);
    }
}
