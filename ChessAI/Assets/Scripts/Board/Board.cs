using UnityEngine;
using UnityEngine.UI;

public enum CellState
{
    None,
    Friendly,
    Enemy,
    Free,
    OutOfBounds
}

public class Board : MonoBehaviour
{
    public GameObject mCellPrefab;

    public Color darkColor;

    public Transform cellHolder;

    [HideInInspector]
    public Cell[,] mAllCells = new Cell[8, 8];

    // Create Board
    public void Create()
    {
        // Create Cells
        for (int y = 0; y < 8; y++)
        {
            for (int x = 0; x < 8; x++)
            {
                // Create the cell
                GameObject newCell = (GameObject)Instantiate(mCellPrefab, transform);

                // Parenting
                newCell.transform.SetParent(cellHolder);

                // Position
                RectTransform rectTransform = newCell.GetComponent<RectTransform>();
                rectTransform.anchoredPosition = new Vector2((x * 100) + 50, (y * 100) + 50);

                // Setup
                mAllCells[x, y] = newCell.GetComponent<Cell>();
                mAllCells[x, y].Setup(new Vector2Int(x, y), this);
            }
        }

        // Color and offset
        for (int y = 0; y < 8; y += 2)
        {
            for (int x = 0; x < 8; x++)
            {
                // Offset for every other line
                int offset = (x % 2 == 0) ? 0 : 1;
                int finalY = y + offset;

                // Color
                mAllCells[x, finalY].GetComponent<Image>().color = darkColor;
            }
        }
    }

    public CellState ValidateCell(int targetX, int targetY, BasePiece checkingPiece)
    {
        // Bounds Check
        if (targetX < 0 || targetX > 7 || targetY < 0 || targetY > 7)
        {
            return CellState.OutOfBounds;
        }

        // Get Cell
        Cell targetCell = mAllCells[targetX, targetY];

        // If Cell Has Piece
        if (targetCell.mCurrentPiece != null)
        {
            // If Friendly Else If Enemy
            if (checkingPiece.mColor == targetCell.mCurrentPiece.mColor)
            {
                return CellState.Friendly;
            }
            else
            {
                return CellState.Enemy;
            }
        }

        // Otherwise Return Free
        return CellState.Free;
    }

    public void ClearHighlighting()
    {
        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                if (mAllCells[i, j].mCurrentPiece != null)
                {
                    mAllCells[i, j].mCurrentPiece.ClearCells();
                }                    
            }
        }
    }
}
