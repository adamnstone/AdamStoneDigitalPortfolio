using UnityEngine;
using UnityEngine.UI;

public class AtBeginningHighScore : MonoBehaviour
{

    public Text highScore;
    // Start is called before the first frame update
    void Start()
    {
        highScore.text = PlayerPrefs.GetInt("HighScore").ToString();
    }
}
