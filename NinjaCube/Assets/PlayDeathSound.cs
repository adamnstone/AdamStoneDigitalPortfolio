using UnityEngine;

public class PlayDeathSound : MonoBehaviour
{
    void TriggerDeathSound()
    {
        AudioManager.mainManager.Stop("Theme");
        AudioManager.mainManager.Play("GameOver");
    }
}
