using UnityEngine;
using UnityEngine.SceneManagement;

public class ToHomeScreen : MonoBehaviour
{
    public void HomeScreen()
    {
        Time.timeScale = 1;
        AudioManager.mainManager.Stop("Theme");
        SceneManager.LoadScene(0);
    }
}
