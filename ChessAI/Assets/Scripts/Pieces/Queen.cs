using UnityEngine;
using UnityEngine.UI;

public class Queen : BasePiece
{
    public override void Setup(Color newTeamColor, Color newSpriteColor, PieceManager newPieceManager)
    {
        // Base Setup
        base.Setup(newTeamColor, newSpriteColor, newPieceManager);

        // Queen Stuff
        mMovement = new Vector3Int(7, 7, 7);
        GetComponent<Image>().sprite = Resources.Load<Sprite>("T_Queen");
    }
}
