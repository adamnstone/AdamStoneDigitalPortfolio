using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnChallenges : MonoBehaviour
{
    public GameObject coin;
    public GameObject enemy;
    public GameObject ramp;
    public GameObject swordPowerup;
    public float[] xPositions;
    public float spawnCounter;
    public float spawnDistance;
    public Transform player;
    float originalCounter;
    float enemyYPosition;
    float coinYPosition;
    float rampYPosition;
    float swordPowerupYPosition = 1.2f;

    void Start()
    {
        originalCounter = spawnCounter;
        enemyYPosition = 1f;
        coinYPosition = 1.5f;
        rampYPosition = 0.75f;
    }
    void Update()
    {
        spawnCounter -= 1 * Time.deltaTime;
        if (spawnCounter <= 0)
        {
            ResetCounter();
            spawn();
        }
    }
    void ResetCounter()
    {
        spawnCounter = originalCounter;
    }

    void spawn()
    {
        for (int i = 0; i < xPositions.Length; i++)
        {
            int rand = Random.Range(1, 101);
            if (rand <= 40) {
                //coins[i].transform.GetChild(0).gameObject.transform.GetChild(0).gameObject.GetComponent<MeshRenderer>().enabled = true;
                Instantiate(coin, position: new Vector3(xPositions[i], coinYPosition, player.position.z + spawnDistance), Quaternion.identity);
            }
            else if (rand <= 80)
            {
                Instantiate(enemy, position: new Vector3(xPositions[i], enemyYPosition, player.position.z + spawnDistance), Quaternion.identity);
            }
            else if (rand <= 85) 
            {
                Instantiate(ramp, position: new Vector3(xPositions[i], rampYPosition, player.position.z + spawnDistance), Quaternion.Euler(new Vector3(55, 0, 0)));
            }
            else if (rand <= 86)
            {
                Instantiate(swordPowerup, position: new Vector3(xPositions[i], swordPowerupYPosition, player.position.z + spawnDistance), Quaternion.Euler(new Vector3(-90, -90, 0)));
            }
        }
    }
}
