using UnityEngine;
using UnityEngine.UI;

public class Rook : BasePiece
{
    public override void Setup(Color newTeamColor, Color newSpriteColor, PieceManager newPieceManager)
    {
        // Base Setup
        base.Setup(newTeamColor, newSpriteColor, newPieceManager);

        // Rook Stuff
        mMovement = new Vector3Int(7, 7, 0);
        GetComponent<Image>().sprite = Resources.Load<Sprite>("T_Rook");
    }
}
