using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GongScript : MonoBehaviour
{
    [HideInInspector]
    public bool high = false;

    public void Gong()
    {
        if (high)
        {
            AudioManager.mainManager.Stop("GameOver");
            AudioManager.mainManager.Play("GongSoundEffect");
        }
    }
}
