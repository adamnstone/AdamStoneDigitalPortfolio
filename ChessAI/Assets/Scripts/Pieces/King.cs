using UnityEngine;
using UnityEngine.UI;

public class King : BasePiece
{
    public override void Setup(Color newTeamColor, Color newSpriteColor, PieceManager newPieceManager)
    {
        // Base Setup
        base.Setup(newTeamColor, newSpriteColor, newPieceManager);

        // King Stuff
        mMovement = new Vector3Int(1, 1, 1);
        GetComponent<Image>().sprite = Resources.Load<Sprite>("T_King");
        
    }

    public override void Kill()
    {
        base.Kill();

        mPieceManager.mIsKingAlive = false;
    }

    public override bool IsKing()
    {
        return true;
    }

    public override void AssignPositionToPieceManager()
    {
        if (mIsWhite)
        {
            mPieceManager.mWhiteKingPosition = mCurrentCell.mBoardPosition;
        }
        else
        {
            mPieceManager.mBlackKingPosition = mCurrentCell.mBoardPosition;
        }
    }
}
