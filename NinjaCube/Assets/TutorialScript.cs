using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class TutorialScript : MonoBehaviour
{
    public GameObject[] steps;
    public GameObject main;
    void Start()
    {
        StartCoroutine(Tutorial());
    }

    IEnumerator Tutorial()
    {
        steps[0].SetActive(true);
        Time.timeScale = 0;
        while (true)
        {
            if (Input.GetKeyDown("left") || Input.GetKeyDown("right"))
            {
                break;
            }
            yield return null;
        }
        Time.timeScale = 1;
        steps[0].SetActive(false);
        main.SetActive(false);
        yield return new WaitForSeconds(2);
        main.SetActive(true);
        steps[1].SetActive(true);
        AudioManager.mainManager.Play("CoinCollect");
        Time.timeScale = 0;
        while (true)
        {
            yield return null;
            if (Input.GetKeyDown("space"))
            {
                break;
            }
        }
        steps[1].SetActive(false);
        steps[2].SetActive(true);
        AudioManager.mainManager.Play("CoinCollect");
        while (true)
        {
            yield return null;
            if (Input.GetKeyDown("space"))
            {
                break;
            }
        }
        steps[2].SetActive(false);
        steps[3].SetActive(true);
        AudioManager.mainManager.Play("CoinCollect");
        while (true)
        {
            yield return null;
            if (Input.GetKeyDown("space"))
            {
                break;
            }
        }
        steps[3].SetActive(false);
        steps[4].SetActive(true);
        AudioManager.mainManager.Play("CoinCollect");
        while (true)
        {
            yield return null;
            if (Input.GetKeyDown("space"))
            {
                break;
            }
        }
        steps[4].SetActive(false);
        steps[5].SetActive(true);
        AudioManager.mainManager.Play("CoinCollect");
        while (true)
        {
            yield return null;
            if (Input.GetKeyDown("space"))
            {
                break;
            }
        }
        Time.timeScale = 1;
        SceneManager.LoadScene(0);
    }
}