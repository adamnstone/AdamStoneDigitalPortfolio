using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayCoinSound : MonoBehaviour
{
    private AudioManager audioManager;

    void Start()
    {
        audioManager = AudioManager.mainManager;
    }

    public void playCoinSound()
    {
        audioManager.Play("CoinCollect");
    }
}
