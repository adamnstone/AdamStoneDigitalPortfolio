using UnityEngine;

public class StorePositionsAndMoves 
{
    public int[,] moves;
    public int[,] originalPositions;
    public StorePositionsAndMoves(int[,] originalPositions_, int[,] moves_)
    {
        originalPositions = originalPositions_;
        moves = moves_;
    }
}
