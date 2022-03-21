using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using System.Collections.Generic;
using System.Collections;

public abstract class BasePiece : EventTrigger
{
    [HideInInspector]
    public Color mColor = Color.clear;

    protected Cell mOriginalCell = null;
    public Cell mCurrentCell = null;

    protected RectTransform mRectTransform = null;
    protected PieceManager mPieceManager;

    public Cell mTargetCell = null;

    protected Vector3Int mMovement = Vector3Int.one;
    public bool mIsFirstMove = true;
    public bool mShouldRestoreFirstMove = true;
    [HideInInspector]
    public string mLetter;
    [HideInInspector]
    public bool mIsWhite;

    public List<Cell> mHighlightedCells = new List<Cell>();

    public virtual void Setup(Color newTeamColor, Color newSpriteColor, PieceManager newPieceManager)
    {
        // Assigning Variables
        mColor = newTeamColor;
        mPieceManager = newPieceManager;
        GetComponent<Image>().color = newSpriteColor;
        mRectTransform = GetComponent<RectTransform>();
        mIsWhite = newTeamColor == Color.white;
    }

    public virtual bool IsPawn()
    {
        return false;
    }

    public virtual bool IsKing()
    {
        return false;
    }

    public void Place(Cell newCell)
    {
        // Cell Assigning
        mOriginalCell = newCell;
        mCurrentCell = newCell;
        mCurrentCell.mCurrentPiece = this;

        // Object Setup
        transform.position = newCell.transform.position;
        gameObject.SetActive(true);

        // Give Piece Manager King Position
        AssignPositionToPieceManager();
    }

    private void CreateCellPath(int xDirection, int yDirection, int movement)
    {
        // Target Position
        int currentX = mCurrentCell.mBoardPosition.x;
        int currentY = mCurrentCell.mBoardPosition.y;

        // Check Each Cell
        for (int i = 1; i <= movement; i++)
        {
            // Change Position
            currentX += xDirection;
            currentY += yDirection;

            // Get State of Target Cell
            CellState cellState = mCurrentCell.mBoard.ValidateCell(currentX, currentY, this);

            // If Cell Is Enemy Add To List And Break; If Cell Is Not Free Break
            if (cellState == CellState.Enemy)
            {
                mHighlightedCells.Add(mCurrentCell.mBoard.mAllCells[currentX, currentY]);
                break;
            }
            else if (cellState != CellState.Free)
                break;


            // Add To List
            mHighlightedCells.Add(mCurrentCell.mBoard.mAllCells[currentX, currentY]);
        }
    }

    public virtual void CheckPathing(bool human = false)
    {
        // Clear Cells
        ClearCells();

        // Horizontal
        CreateCellPath(1, 0, mMovement.x);
        CreateCellPath(-1, 0, mMovement.x);

        // Vertical
        CreateCellPath(0, 1, mMovement.y);
        CreateCellPath(0, -1, mMovement.y);

        // Upper Diagonal
        CreateCellPath(1, 1, mMovement.z);
        CreateCellPath(-1, 1, mMovement.z);

        // Lower Diagonal
        CreateCellPath(-1, -1, mMovement.z);
        CreateCellPath(1, -1, mMovement.z);
    }

    protected void ShowCells()
    {
        foreach (Cell cell in mHighlightedCells)
            cell.mOutlineImage.enabled = true;
    }

    public virtual void ClearCells()
    {
        foreach (Cell cell in mHighlightedCells)
            cell.mOutlineImage.enabled = false;

        mHighlightedCells.Clear();
    }

    public virtual void Reset()
    {
        Kill();

        Place(mOriginalCell);
    }

    public virtual void Kill()
    {
        // Clear Current Cell
        mCurrentCell.mCurrentPiece = null;

        // Remove Piece
        gameObject.SetActive(false);
    }

    public virtual void AssignPositionToPieceManager()
    {

    }

    public virtual IEnumerator Move(bool takeAwayGiveBack = true, bool delayedMovement = true)
    {
        if (mTargetCell.mCurrentPiece != null)
        {
            if (mTargetCell.mCurrentPiece.IsKing())
            {
                mPieceManager.mGameIsOver = true;
            }
        }

        if (mTargetCell.mCurrentPiece != null)
        {
            mPieceManager.mTotalPieceCount--;
            if (mLetter != "P")
            {
                mPieceManager.mRoyaltyCount--;
            }
            if (!mTargetCell.mCurrentPiece.IsKing())
            {
                mPieceManager.mCountLibrary[mTargetCell.mCurrentPiece.mLetter]--;
                if (mTargetCell.mCurrentPiece.mIsWhite)
                {
                    mPieceManager.mWhiteCountLibrary[mTargetCell.mCurrentPiece.mLetter]--;
                }
            }
        }

        // Remove Enemy Piece
        mTargetCell.RemovePiece();

        // Clear Current
        mCurrentCell.mCurrentPiece = null;

        // Switch Cells
        mCurrentCell = mTargetCell;
        
        mCurrentCell.mCurrentPiece = this;

        if (IsKing())
        {
            AssignPositionToPieceManager();
        }

        if (delayedMovement)
        {
            while (Vector2.Distance(transform.position, mCurrentCell.transform.position) > mPieceManager.mComputerMovementLeeway)
            {
                transform.position = Vector2.MoveTowards(transform.position, mCurrentCell.transform.position, mPieceManager.mPieceSpeed * Time.deltaTime);
                yield return new WaitForSeconds(Time.deltaTime);
            }
        }
        else
        {
            transform.position = mCurrentCell.transform.position;
        }

        mTargetCell = null;

        if (mIsFirstMove)
        {
            mIsFirstMove = false;
            mShouldRestoreFirstMove = !takeAwayGiveBack;
        }
    }

    public override void OnBeginDrag(PointerEventData eventData)
    {
        base.OnBeginDrag(eventData);

        // Test For Cells
        CheckPathing(human: true);

        // Highlight cells
        ShowCells();
    }

    public override void OnDrag(PointerEventData eventData)
    {
        base.OnDrag(eventData);

        // Follow Mouse
        transform.position += (Vector3)eventData.delta;

        // Check For Overlapping Available Squares
        foreach (Cell cell in mHighlightedCells)
        {
            if (RectTransformUtility.RectangleContainsScreenPoint(cell.mRectTransform, Input.mousePosition))
            {
                // If Mouse is Over Cell Set As Target Cell And Break
                mTargetCell = cell;
                break;
            }
            // Mouse Not Withing Highlighted Cell
            mTargetCell = null;
        }
    }

    public override void OnEndDrag(PointerEventData eventData)
    {
        base.OnEndDrag(eventData);

        // Clear Cell Highlighting
        ClearCells();

        // Return To Original Position If No Target Cell Or If Move Is Invalid
        if (!mTargetCell || !mPieceManager.ValidateMove(this, mTargetCell.mBoardPosition.x, mTargetCell.mBoardPosition.y))
        {
            transform.position = mCurrentCell.transform.position;
            return;
        }

        // Move To New Cell
        StartCoroutine(Move(delayedMovement: false));

        // Switch Sides
        mPieceManager.SwitchSides(mColor == Color.white);
    }

}
