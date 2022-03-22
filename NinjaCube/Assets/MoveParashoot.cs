using UnityEngine;

public class MoveParashoot : MonoBehaviour
{
    public Vector3 offset;
    [System.NonSerialized]
    public bool show;
    public Transform player;

    // Update is called once per frame
    void Update()
    {
    transform.position = player.position + offset;
    }
}
