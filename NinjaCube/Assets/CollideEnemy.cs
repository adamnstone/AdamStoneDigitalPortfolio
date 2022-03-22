using UnityEngine.UI;
using UnityEngine;

public class CollideEnemy : MonoBehaviour
{
    public PlayerMovement movement;
    public float delayToEnd = 1f;
    [System.NonSerialized]
    public bool canDefeatEnemies = false;
    public GameObject gameOverUI;
    bool gameEnded = false;
    public GameObject backButton;
    Collider tempCollision;
    public Text points;
    public Text highPoints;
    public Text scoreAtEndWord;
    public GongScript gongScript;
    public Text scoreAtEnd;

    void OnCollisionEnter(Collision colliderInfo)
    {
        if (colliderInfo.collider.tag == "Enemy")
        {
            if (!canDefeatEnemies)
            {
                movement.enabled = false;
                Invoke("EndGame", delayToEnd);
                AudioManager.mainManager.Play("DeathSoundEffect");
            }
            else
            {
                AudioManager.mainManager.RandomizePitch("KillEnemySoundEffect", 0.15f);
                AudioManager.mainManager.Play("KillEnemySoundEffect");
                int parsed;
                bool worked = int.TryParse(points.text, out parsed);
                if (worked)
                {
                    points.text = (parsed + 3).ToString();
                    if (parsed + 1 > PlayerPrefs.GetInt("HighScore"))
                    {
                        highPoints.text = (parsed + 3).ToString();
                        PlayerPrefs.SetInt("HighScore", parsed + 3);
                        scoreAtEndWord.text = "<b>New High Score!</b>";
                        gongScript.high = true;
                    }
                    scoreAtEnd.text = (parsed + 3).ToString();
                }
                colliderInfo.collider.GetComponent<MeshRenderer>().enabled = false;
                colliderInfo.collider.GetComponent<BoxCollider>().enabled = false;
                tempCollision = colliderInfo.collider;
                MeshRenderer[] quads = { colliderInfo.collider.gameObject.transform.GetChild(0).gameObject.GetComponent<MeshRenderer>(), colliderInfo.collider.gameObject.transform.GetChild(1).gameObject.GetComponent<MeshRenderer>() };
                foreach (MeshRenderer mr in quads)
                {
                    mr.enabled = false;
                }
                Invoke("ShowObject", 2f);
            }
        }
    }

    public void EndGame()
    {
        if (!gameEnded)
        {
            AudioManager.mainManager.Stop("Theme");
            gameEnded = true;
            backButton.SetActive(false);
            gameOverUI.SetActive(true);
        }
    }

    void ShowObject()
    {
        //tempCollision.GetComponent<MeshRenderer>().enabled = true;
        //tempCollision.GetComponent<BoxCollider>().enabled = true;
        //MeshRenderer[] quads = { tempCollision.gameObject.transform.GetChild(0).gameObject.GetComponent<MeshRenderer>(), tempCollision.gameObject.transform.GetChild(1).gameObject.GetComponent<MeshRenderer>() };
        //foreach (MeshRenderer mr in quads)
        //{
            //mr.enabled = true;
        //}
    }
}