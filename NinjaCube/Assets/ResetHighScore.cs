using UnityEngine;

public class ResetHighScore : MonoBehaviour
{
    // Start is called before the first frame update
    public void ResetHigh()
    {
        PlayerPrefs.SetInt("HighScore", 0);
    }
}
