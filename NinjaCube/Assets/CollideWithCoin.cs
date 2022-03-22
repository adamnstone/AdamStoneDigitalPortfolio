using UnityEngine;
using UnityEngine.UI;

public class CollideWithCoin : MonoBehaviour
{

    public Text points;
    public float forceIncreasePerCoin = 10f;
    private AudioManager audioManager;
    public PlayerMovement player;
    public Text highPoints;
    public MeshRenderer mesh;
    public BoxCollider box;
    public Text scoreAtEndWord;
    public Text scoreAtEnd;
    public float visibleWaiting = 2f;
    public float maxSpeed = 175f;
    public GongScript gongScript;

    void Start()
    {
        audioManager = AudioManager.mainManager;
    }
    
    void OnTriggerEnter(Collider colliderInfo)
    {
        if (colliderInfo.GetComponent<Collider>().tag == "Player")
        {
            if (player.forwardsForce <= maxSpeed)
            {
                player.forwardsForce += forceIncreasePerCoin;
                player.sidewaysForce += forceIncreasePerCoin;
            }
            audioManager.IncreasePitch("Theme");
            audioManager.Play("CoinCollect");
            int parsed;
            bool worked = int.TryParse(points.text, out parsed);
            if (worked)
            {
                points.text = (parsed + 1).ToString();
                if (parsed + 1 > PlayerPrefs.GetInt("HighScore"))
                {
                    highPoints.text = (parsed + 1).ToString();
                    PlayerPrefs.SetInt("HighScore", parsed + 1);
                    scoreAtEndWord.text = "<b>New High Score!</b>";
                    gongScript.high = true;
                }
                scoreAtEnd.text = (parsed + 1).ToString();
            }
            box.enabled = false;
            mesh.enabled = false;
            Invoke("makeVisible", visibleWaiting);
        }
    }

    void makeVisible()
    {
        mesh.enabled = true;
        box.enabled = true;
    }
}

