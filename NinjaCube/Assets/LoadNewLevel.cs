using UnityEngine.SceneManagement;
using UnityEngine;

public class LoadNewLevel : MonoBehaviour
{
    public void LoadNewScene()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }
}
