@Entity
@Table(name="comment")
public class Comment implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private long commentId;

    @Column(name="user_id")
    private long userId;

    @Column(name="content")
    private String content;

    @Column(name="date_created")
    private Date dateCreated;

}

