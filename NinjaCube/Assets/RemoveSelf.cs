using UnityEngine;

public class RemoveSelf : MonoBehaviour
{
    public Transform player;
    public float removeDistance = 6f;
    void Update()
    {
        if (transform.position.z < player.position.z - removeDistance && transform.position.z > 20f) 
        {
            Destroy(gameObject);
        }
    }
}
