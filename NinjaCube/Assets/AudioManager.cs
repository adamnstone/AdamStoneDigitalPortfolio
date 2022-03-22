using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.Audio;
using System;

public class AudioManager : MonoBehaviour
{
    public Sound[] sounds;
    public float pitchIncrease;
    public static AudioManager mainManager;
    public static bool hasMainManager = false;
    public float themePitch;
    private float deathPitch;

    void Awake()
    {
        themePitch = 1.55f;
        deathPitch = 1f;
        if (!AudioManager.hasMainManager)
        {
            mainManager = this;
            hasMainManager = true;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            AudioManager.mainManager.Start();
            Destroy(gameObject);
        }
        foreach (Sound s in sounds)
        {
            s.source = gameObject.AddComponent<AudioSource>();
            s.source.clip = s.clip;
            s.source.volume = s.volume;
            s.source.pitch = s.pitch;
            s.source.loop = s.loop;
        }
    }

    void Start()
    {
        string name = SceneManager.GetActiveScene().name;
        if (name != "HomeScreen")
        {
            Stop("NinjaSoundEffect");
        }
        if (name == "Game")
        {
            SetPitch("Theme", AudioManager.mainManager.themePitch);
            SetPitch("DeathSoundEffect", AudioManager.mainManager.deathPitch);
            Stop("GongSoundEffect");
            Play("Theme");
        }
        else if (name == "ResetScore")
        {
            Play("GongSoundEffect");
        }
        else if (name == "HomeScreen")
        {
            Stop("GongSoundEffect");
            Play("NinjaSoundEffect");
        }
        else
        {
            Stop("NinjaSoundEffect");
        }
    }

    public void Play(string name)
    {
        Sound s = Array.Find(sounds, sound => sound.name == name);
        if (s == null)
        {
            Debug.LogWarning($"Sound {name} not found :(");
            return;
        }
        s.source.Play();
    }

    public void Stop(string name)
    {
        Sound s = Array.Find(sounds, sound => sound.name == name);
        if (s == null)
        {
            Debug.LogWarning($"Sound {name} not found :(");
            return;
        }
        s.source.Stop();
    }

    public void IncreasePitch(string name)
    {
        Sound s = Array.Find(sounds, sound => sound.name == name);
        if (s == null)
        {
            Debug.LogWarning($"Sound {name} not found :(");
            return;
        }
        s.source.pitch += pitchIncrease;
    }

    public void SetPitch(string name, float pitch)
    {
        Sound s = Array.Find(sounds, sound => sound.name == name);
        if (s == null)
        {
            Debug.LogWarning($"Sound {name} not found :(");
            return;
        }
        s.source.pitch = pitch;
    }

    public void RandomizePitch(string name, float amount)
    {
        Sound s = Array.Find(sounds, sound => sound.name == name);
        if (s == null)
        {
            Debug.LogWarning($"Sound {name} not found :(");
            return;
        }
        s.source.pitch = s.source.pitch + UnityEngine.Random.Range(-amount, amount);
    }
}
