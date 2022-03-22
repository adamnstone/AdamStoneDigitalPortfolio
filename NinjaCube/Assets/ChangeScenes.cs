using UnityEngine;
using UnityEngine.SceneManagement;

public class ChangeScenes : MonoBehaviour
{
    public void Play()
    {
        SceneManager.LoadScene("Game");
    }

    public void Credits()
    {
        SceneManager.LoadScene("Credits");
    }

    public void Tutorial()
    {
        SceneManager.LoadScene("Tutorial");
    }

    public void ResetScore()
    {
        SceneManager.LoadScene("ResetScore");
    }
}
