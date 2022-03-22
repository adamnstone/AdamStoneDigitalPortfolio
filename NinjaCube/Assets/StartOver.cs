using UnityEngine;
using UnityEngine.SceneManagement;

public class StartOver : MonoBehaviour
{
    public void NewGame()
    {
        Time.timeScale = 1;
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }
}
